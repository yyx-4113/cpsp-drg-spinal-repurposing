# -*- coding: utf-8 -*-
"""P6 标书 V5 收尾补丁：清理主模型名残留（§5.3 动物模型条、§10.4 预实验）。"""
import io
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
DST = os.path.join(BASE, 'P6_FJNSF_APPLICATION_SUBMISSION_V5.md')

EDITS = [
    (
        '''- **动物模型**：足底切口痛与 SNI 均为成熟模型，重复性好；切口痛模型与''',
        '''- **动物模型**：SMIR 与 SNI 均为成熟模型，重复性好；SMIR 与''',
        '§5.3 动物模型条前半',
    ),
    (
        '''本条修订要点：主模型已由足底切口痛改为 **SMIR**——其痛觉超敏可持续约 3–4 周、可覆盖 d3–d28 全时程''',
        '''本条要点：SMIR 的痛觉超敏可持续约 3–4 周、可覆盖 d3–d28 全时程''',
        '§5.3 动物模型条后半',
    ),
    (
        '''为使关键技术（切口痛模型制备、鞘内给药、qPCR 与 IHC 检测）''',
        '''为使关键技术（SMIR 建模、鞘内给药、qPCR 与 IHC 检测）''',
        '§10.4 预实验技术项',
    ),
    (
        '''检测 `Adra2a` 与 5–8 个代表性 hub 基因的 mRNA 变化''',
        '''检测 `Adra2a`、5 个代表性 hub（`Atf3`、`Npy`、`Ecel1`、`Serpine1`、`Cdhr5`）及 3 个核心签名基因（`Gal`、`Vgf`、`Socs3`）的 mRNA 变化''',
        '§10.4 预实验基因面板',
    ),
]


def main():
    with io.open(DST, 'r', encoding='utf-8') as f:
        text = f.read()
    for old, new, tag in EDITS:
        n = text.count(old)
        if n != 1:
            print('[FAIL] %-28s 命中 %d 次（应为 1 次）' % (tag, n))
            return 1
        text = text.replace(old, new, 1)
        print('[ OK ] %s' % tag)
    with io.open(DST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('\n收尾补丁完成，剩余“足底切口痛”出现次数：%d（应均为退守方案/修订说明中的正常提及）' % text.count('足底切口痛'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
