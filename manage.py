import click
from backup import BackupManager
from pathlib import Path
import sys
import logging
import shutil
from datetime import datetime
import json

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

backup_manager = BackupManager()

def validate_version(ctx, param, value):
    """验证版本号格式"""
    if value and not value.replace(".", "").isdigit():
        raise click.BadParameter('版本号必须是数字和点组成，如 1.0.0')
    return value

def get_project_files():
    """获取项目文件列表"""
    return [
        "main.py",
        "backup.py",
        "manage.py",
        "templates/index.html",
        "CHANGELOG.md",
        "locales/en_US.yml",
        "locales/zh_CN.yml"
    ]

def check_project_status():
    """检查项目状态"""
    status = {
        "files": {},
        "directories": {},
        "total_files": 0,
        "missing_files": 0
    }
    
    # 检查目录
    required_dirs = ["templates", "locales", "downloads", "backups"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        exists = dir_path.exists() and dir_path.is_dir()
        status["directories"][dir_name] = exists
    
    # 检查文件
    for file_path in get_project_files():
        path = Path(file_path)
        exists = path.exists() and path.is_file()
        status["files"][file_path] = exists
        status["total_files"] += 1
        if not exists:
            status["missing_files"] += 1
    
    return status

@click.group()
def cli():
    """YouTube 下载器项目管理工具"""
    pass

@cli.command()
@click.option('--version', prompt='版本号', callback=validate_version, 
              help='备份的版本号 (例如: 1.0.0)')
@click.option('--description', prompt='备份描述', 
              help='备份的描述信息')
@click.option('--force', is_flag=True, 
              help='强制创建备份，即使文件不完整')
def backup(version, description, force):
    """创建项目备份"""
    try:
        # 检查项目状态
        status = check_project_status()
        
        if status["missing_files"] > 0 and not force:
            logger.error("❌ 以下文件缺失:")
            for file, exists in status["files"].items():
                if not exists:
                    logger.error(f"  - {file}")
            logger.error("使用 --force 选项可以强制创建备份")
            return
        
        # 更新 CHANGELOG.md
        changelog_path = Path("CHANGELOG.md")
        if changelog_path.exists():
            with open(changelog_path, "r+", encoding="utf-8") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"""# 更新日志

## [{version}] - {datetime.now().strftime('%Y-%m-%d')}

### 更新内容
- {description}

{content}""")
        
        # 创建备份
        if backup_manager.create_backup(version, description):
            logger.info(f"✅ 备份创建成功")
            logger.info(f"  版本: {version}")
            logger.info(f"  描述: {description}")
            logger.info(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"  文件: {status['total_files'] - status['missing_files']}/{status['total_files']}")
        else:
            logger.error("❌ 备份创建失败")
            
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

@cli.command()
@click.option('--version', callback=validate_version,
              help='要恢复的版本号，不指定则使用最新版本')
@click.option('--force', is_flag=True,
              help='强制恢复，不创建临时备份')
def restore(version, force):
    """恢复项目备份"""
    try:
        if not force:
            # 创建临时备份
            temp_version = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info("📦 创建临时备份...")
            backup_manager.create_backup(temp_version, "恢复前的自动备份")
        
        if backup_manager.restore_backup(version):
            logger.info(f"✅ 备份恢复成功 {'(最新版本)' if not version else f'(版本 {version})'}")
            logger.info("🔄 请重启应用以应用更改")
        else:
            logger.error("❌ 恢复失败")
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

@cli.command()
@click.option('--all', is_flag=True, help='显示所有详细信息')
@click.option('--json', 'output_json', is_flag=True, help='以 JSON 格式输出')
def list(all, output_json):
    """列出所有备份"""
    try:
        backups = backup_manager.get_backup_list()
        if not backups:
            logger.info("💡 没有找到任何备份")
            return
        
        if output_json:
            print(json.dumps(backups, indent=2, ensure_ascii=False))
            return
        
        logger.info("\n📋 备份列表:")
        for backup in sorted(backups, key=lambda x: x['timestamp'], reverse=True):
            if all:
                logger.info(f"""
🔹 版本: {backup['version']}
  时间: {backup['timestamp']}
  描述: {backup['description']}
  路径: {backup['path']}
  文件: {', '.join(backup['files'])}
{'='*50}""")
            else:
                logger.info(f"🔹 {backup['version']} - {backup['description']} ({backup['timestamp']})")
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

@cli.command()
@click.option('--keep', type=int, default=5,
              help='要保留的备份数量 (默认: 5)')
@click.confirmation_option(prompt='确定要清理旧备份吗？')
def clean(keep):
    """清理旧备份，默认保留最近5个"""
    try:
        backup_manager._cleanup_old_backups(keep)
        logger.info(f"✅ 清理完成，保留了最新的 {keep} 个备份")
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

@cli.command()
@click.argument('version')
@click.confirmation_option(prompt='确定要删除这个备份吗？')
def delete(version):
    """删除指定版本的备份"""
    try:
        backups = [b for b in backup_manager.get_backup_list() if b['version'] == version]
        if not backups:
            logger.error(f"❌ 未找到版本 {version} 的备份")
            return
        
        for backup in backups:
            if backup_manager.delete_backup(backup['version'], backup['timestamp']):
                logger.info(f"✅ 已删除版本 {version} 的备份")
            else:
                logger.error(f"❌ 删除版本 {version} 的备份失败")
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

@cli.command()
def status():
    """检查项目状态"""
    try:
        status = check_project_status()
        
        logger.info("\n📊 项目状态:")
        
        logger.info("\n目录:")
        for dir_name, exists in status["directories"].items():
            logger.info(f"{'✅' if exists else '❌'} {dir_name}")
        
        logger.info("\n文件:")
        for file_path, exists in status["files"].items():
            logger.info(f"{'✅' if exists else '❌'} {file_path}")
        
        logger.info(f"\n总计: {status['total_files'] - status['missing_files']}/{status['total_files']} 个文件")
    except Exception as e:
        logger.error(f"❌ 错误: {e}")

if __name__ == '__main__':
    cli() 