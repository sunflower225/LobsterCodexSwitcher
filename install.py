#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LobsterCodexSwitcher 安装脚本

支持平台: macOS, Linux, Windows
"""

import os
import sys
import platform
import shutil
from pathlib import Path

def get_colors():
    """获取终端颜色支持"""
    supports_color = (
        hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
        (platform.system() != 'Windows' or 'ANSICON' in os.environ or
         'WT_SESSION' in os.environ or os.environ.get('TERM') == 'xterm')
    )

    if supports_color:
        class Colors:
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            CYAN = '\033[96m'
            BOLD = '\033[1m'
            DIM = '\033[2m'
            ENDC = '\033[0m'
        return Colors
    else:
        class Colors:
            GREEN = YELLOW = RED = CYAN = BOLD = DIM = ENDC = ''
        return Colors

Colors = get_colors()

def get_script_dir():
    """获取脚本所在目录"""
    return Path(__file__).parent.resolve()

def get_install_dir():
    """获取安装目录"""
    home = Path.home()
    if platform.system() == "Windows":
        return home / "codex-switcher"
    else:
        return home / "codex-switcher"

def get_bin_dir():
    """获取可执行文件目录"""
    home = Path.home()
    if platform.system() == "Windows":
        # Windows: 使用用户目录下的 bin
        return home / "bin"
    else:
        # macOS/Linux: 使用 ~/.local/bin 或 ~/bin
        local_bin = home / ".local" / "bin"
        if local_bin.exists():
            return local_bin
        return home / "bin"

def get_shell_config():
    """获取 shell 配置文件"""
    home = Path.home()
    shell = os.environ.get('SHELL', '')

    if 'zsh' in shell:
        return home / ".zshrc"
    elif 'bash' in shell:
        # 优先使用 .bashrc，macOS 可能使用 .bash_profile
        bashrc = home / ".bashrc"
        if bashrc.exists():
            return bashrc
        return home / ".bash_profile"
    else:
        return home / ".profile"

def install():
    """安装 codex-switcher"""
    script_dir = get_script_dir()
    install_dir = get_install_dir()
    bin_dir = get_bin_dir()

    print(f"{Colors.BOLD}LobsterCodexSwitcher 安装程序{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.ENDC}\n")

    # 1. 创建安装目录
    print(f"{Colors.CYAN}[1/4] 创建安装目录...{Colors.ENDC}")
    install_dir.mkdir(parents=True, exist_ok=True)
    (install_dir / "accounts").mkdir(parents=True, exist_ok=True)
    print(f"      {install_dir}")

    # 2. 复制主脚本
    print(f"{Colors.CYAN}[2/4] 复制程序文件...{Colors.ENDC}")
    src_script = script_dir / "codex-switcher.py"
    dst_script = install_dir / "codex-switcher.py"
    src_module = script_dir / "codex_switcher.py"
    dst_module = install_dir / "codex_switcher.py"

    if src_script.exists():
        # 如果源和目标相同，跳过复制
        if src_script.resolve() != dst_script.resolve():
            shutil.copy2(src_script, dst_script)
        # 添加执行权限
        os.chmod(dst_script, 0o755)
        print(f"      {dst_script}")
    else:
        print(f"      {Colors.RED}错误: 找不到源文件{Colors.ENDC}")
        return False

    if src_module.exists():
        if src_module.resolve() != dst_module.resolve():
            shutil.copy2(src_module, dst_module)
        os.chmod(dst_module, 0o755)
        print(f"      {dst_module}")
    else:
        print(f"      {Colors.RED}错误: 找不到模块文件{Colors.ENDC}")
        return False

    # 3. 创建启动脚本
    print(f"{Colors.CYAN}[3/4] 创建命令链接...{Colors.ENDC}")

    if platform.system() == "Windows":
        # Windows: 创建 .cmd 批处理文件
        bin_dir.mkdir(parents=True, exist_ok=True)
        cmd_file = bin_dir / "codex-switcher.cmd"
        with open(cmd_file, 'w') as f:
            f.write(f'@echo off\npython "{dst_script}" %*\n')
        print(f"      {cmd_file}")

        # 提示添加到 PATH
        print(f"\n{Colors.YELLOW}提示: 请将以下目录添加到系统 PATH:{Colors.ENDC}")
        print(f"      {bin_dir}")

    else:
        # macOS/Linux: 创建符号链接或 shell 脚本
        bin_dir.mkdir(parents=True, exist_ok=True)
        link_file = bin_dir / "codex-switcher"

        # 删除旧的链接
        if link_file.exists() or link_file.is_symlink():
            link_file.unlink()

        # 创建启动脚本
        with open(link_file, 'w') as f:
            f.write(f'#!/bin/bash\npython3 "{dst_script}" "$@"\n')
        os.chmod(link_file, 0o755)
        print(f"      {link_file}")

        # 4. 添加到 PATH
        print(f"{Colors.CYAN}[4/4] 配置 PATH 环境变量...{Colors.ENDC}")

        shell_config = get_shell_config()
        path_export = f'export PATH="$PATH:{bin_dir}"'

        if shell_config.exists():
            with open(shell_config, 'r') as f:
                content = f.read()

            if str(bin_dir) not in content:
                with open(shell_config, 'a') as f:
                    f.write(f'\n# LobsterCodexSwitcher\n')
                    f.write(f'{path_export}\n')
                print(f"      {Colors.GREEN}已添加到 {shell_config}{Colors.ENDC}")
            else:
                print(f"      {Colors.DIM}已在 PATH 中{Colors.ENDC}")
        else:
            print(f"      {Colors.DIM}未找到 shell 配置文件{Colors.ENDC}")

    # 安装完成
    print(f"\n{Colors.GREEN}{'═' * 50}{Colors.ENDC}")
    print(f"{Colors.GREEN}  ✓ 安装完成！{Colors.ENDC}")
    print(f"{Colors.GREEN}{'═' * 50}{Colors.ENDC}\n")

    print(f"使用方法:")
    print(f"  1. 重新打开终端（或运行: source {get_shell_config()}）")
    print(f"  2. 运行命令: {Colors.BOLD}codex-switcher{Colors.ENDC}")
    print(f"  3. 或使用简写: {Colors.BOLD}csw{Colors.ENDC}")

    # 创建简写别名
    shell_config = get_shell_config()
    if shell_config.exists() and platform.system() != "Windows":
        with open(shell_config, 'a') as f:
            f.write(f'alias csw="codex-switcher"\n')
        print(f"\n{Colors.DIM}已添加别名 csw -> codex-switcher{Colors.ENDC}")

    return True

def uninstall():
    """卸载 codex-switcher"""
    install_dir = get_install_dir()
    bin_dir = get_bin_dir()

    print(f"{Colors.BOLD}LobsterCodexSwitcher 卸载程序{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.ENDC}\n")

    # 删除安装目录（保留 accounts）
    print(f"{Colors.CYAN}[1/2] 删除程序文件...{Colors.ENDC}")
    script_file = install_dir / "codex-switcher.py"
    if script_file.exists():
        script_file.unlink()
        print(f"      {Colors.GREEN}✓{Colors.ENDC} {script_file}")

    # 删除命令链接
    print(f"{Colors.CYAN}[2/2] 删除命令链接...{Colors.ENDC}")
    link_file = bin_dir / "codex-switcher"
    if link_file.exists():
        link_file.unlink()
        print(f"      {Colors.GREEN}✓{Colors.ENDC} {link_file}")

    print(f"\n{Colors.GREEN}卸载完成！{Colors.ENDC}")
    print(f"{Colors.DIM}已存档的账号数据保留在: {install_dir / 'accounts'}{Colors.ENDC}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--uninstall':
        uninstall()
    else:
        install()
