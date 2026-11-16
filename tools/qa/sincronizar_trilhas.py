"""Teste rápido da sincronização de trilhas e recomendações, sem navegador."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from sincronizar_trilhas import sincronizar
from recomendacoes_adicionais import incluir

MD = '''# Catálogo
## 6. Histórica
| Título | Autor | Tags |
|---|---|---|
| Um | Ana | #F #d1 #e1 #trilha-antiga |
| Dois | Bia | #NF #d2 #e2 |
## 17. Biblioteca virtual
| Título | Autor | Tags |
|---|---|---|
| Três | Caio | #NF #d1 #e1 #trilha-antiga |
'''
TRILHAS = '''## 1. Primeira
`#trilha-um`
1. Um | Ana
2. Três | Caio
## 2. Segunda
`#trilha-dois`
1. Um | Ana
2. Dois | Bia
'''


class Sincronizacao(unittest.TestCase):
    def test_adiciona_remove_preserva_e_repete(self):
        novo, dif = sincronizar(MD, TRILHAS)
        self.assertEqual(len(dif), 3)
        self.assertIn('| Um | Ana | #F #d1 #e1 #trilha-dois #trilha-um |', novo)
        self.assertIn('| Três | Caio | #NF #d1 #e1 #trilha-um |', novo)
        self.assertNotIn('#trilha-antiga', novo)
        self.assertEqual(sincronizar(novo, TRILHAS), (novo, []))

    def test_erros_nao_geram_resultado(self):
        for texto in (TRILHAS.replace('Três | Caio', 'Três | Autor errado'),
                      TRILHAS.replace('`#trilha-dois`', '`#trilha-um`'),
                      TRILHAS.replace('2. Três | Caio', '2. Um | Ana'),
                      '## 1. Sem marcador\n1. Um | Ana\n',
                      '## 1. Sem itens\n`#trilha-vazia`\n'):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                sincronizar(MD, texto)
        with self.assertRaises(ValueError):
            sincronizar(MD.replace('| Dois | Bia |', '| Um | Ana |'), TRILHAS)

    def test_recomendacao_antes_das_trilhas(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp) / 'novos.tsv'
            p.write_text('titulo\tautor\tsecao\ttags\nNovo\tDora\t6\tF d1 e2\n', encoding='utf-8')
            md = incluir(MD, p)
            self.assertEqual(md, incluir(md, p))
            novo, _ = sincronizar(md, '## 1. X\n`#trilha-x`\n1. Novo | Dora\n')
            self.assertIn('| Novo | Dora | #F #d1 #e2 #trilha-x |', novo)


if __name__ == '__main__':
    resultado = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Sincronizacao))
    print('ERROS:', len(resultado.errors) + len(resultado.failures))
    sys.exit(0 if resultado.wasSuccessful() else 1)
