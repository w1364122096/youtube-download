import shutil
from pathlib import Path
import json
from datetime import datetime
import logging
import os

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.backup_info_file = self.backup_dir / "backup_info.json"
        self.load_backup_info()
    
    def load_backup_info(self):
        if self.backup_info_file.exists():
            with open(self.backup_info_file, "r", encoding="utf-8") as f:
                self.backup_info = json.load(f)
        else:
            self.backup_info = {"backups": []}
    
    def save_backup_info(self):
        with open(self.backup_info_file, "w", encoding="utf-8") as f:
            json.dump(self.backup_info, f, indent=2, ensure_ascii=False)
    
    def get_backup_list(self):
        """获取所有备份列表"""
        return self.backup_info["backups"]
    
    def delete_backup(self, version, timestamp):
        """删除指定的备份"""
        for backup in self.backup_info["backups"]:
            if backup["version"] == version and backup["timestamp"] == timestamp:
                try:
                    # 删除备份文件
                    backup_path = Path(backup["path"])
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    
                    # 从列表中移除
                    self.backup_info["backups"].remove(backup)
                    self.save_backup_info()
                    
                    logger.info(f"备份删除成功: {version} ({timestamp})")
                    return True
                except Exception as e:
                    logger.error(f"删除备份失败: {e}")
                    return False
        
        logger.error(f"找不到指定的备份: {version} ({timestamp})")
        return False
    
    def create_backup(self, version, description=""):
        """创建系统备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{version}_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        try:
            # 创建备份目录
            backup_path.mkdir(exist_ok=True)
            
            # 备份主要文件和目录
            files_to_backup = [
                "main.py",
                "backup.py",
                "templates/index.html",
                "locales/zh_CN.yml",
                "locales/en_US.yml",
                "CHANGELOG.md"
            ]
            
            for file in files_to_backup:
                src = Path(file)
                if src.exists():
                    dst = backup_path / src.name
                    dst.parent.mkdir(exist_ok=True)
                    shutil.copy2(src, dst)
            
            # 记录备份信息
            backup_info = {
                "version": version,
                "timestamp": timestamp,
                "description": description,
                "path": str(backup_path),
                "files": files_to_backup,
                "created_at": datetime.now().isoformat()
            }
            
            self.backup_info["backups"].append(backup_info)
            self.save_backup_info()
            
            # 保留最近的5个备份
            self._cleanup_old_backups(5)
            
            logger.info(f"备份创建成功: {backup_name}")
            return True
            
        except Exception as e:
            logger.error(f"创建备份失败: {e}")
            return False
    
    def _cleanup_old_backups(self, keep_count):
        """清理旧备份，只保留最近的几个"""
        if len(self.backup_info["backups"]) > keep_count:
            # 按时间戳排序
            sorted_backups = sorted(
                self.backup_info["backups"],
                key=lambda x: x["timestamp"],
                reverse=True
            )
            
            # 删除旧备份
            for backup in sorted_backups[keep_count:]:
                backup_path = Path(backup["path"])
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                self.backup_info["backups"].remove(backup)
            
            self.save_backup_info()
            logger.info(f"已清理旧备份，保留最新的 {keep_count} 个")
    
    def restore_backup(self, version=None, timestamp=None):
        """恢复系统备份"""
        if not self.backup_info["backups"]:
            logger.error("没有可用的备份")
            return False
        
        # 查找指定的备份
        if version and timestamp:
            matching_backups = [
                b for b in self.backup_info["backups"]
                if b["version"] == version and b["timestamp"] == timestamp
            ]
            if not matching_backups:
                logger.error(f"找不到指定的备份: {version} ({timestamp})")
                return False
            backup = matching_backups[0]
        else:
            # 使用最新的备份
            backup = sorted(
                self.backup_info["backups"],
                key=lambda x: x["timestamp"],
                reverse=True
            )[0]
        
        try:
            # 创建当前状态的临时备份
            self.create_backup("auto_backup", "恢复前的自动备份")
            
            backup_path = Path(backup["path"])
            
            # 恢复文件
            for file in backup["files"]:
                src = backup_path / Path(file).name
                dst = Path(file)
                dst.parent.mkdir(exist_ok=True)
                if src.exists():
                    shutil.copy2(src, dst)
            
            logger.info(f"恢复备份成功: {backup['version']} ({backup['timestamp']})")
            return True
            
        except Exception as e:
            logger.error(f"恢复备份失败: {e}")
            return False 