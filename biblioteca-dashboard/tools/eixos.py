"""Classifica os livros da estante (seção 0) em um dos 16 eixos temáticos do catálogo, a partir das tags."""
def eixo_estante(b):
    T = set(b['tags'])
    has = lambda *xs: any(x in T for x in xs)
    fic = 'F' in T or 'HQ' in T
    nf = 'NF' in T
    if 'poesia' in T and not fic:
        return 8
    if has('pre-historia', 'neandertal'):
        return 1
    if fic:
        if has('horror', 'lovecraftiano'): return 7
        if has('ficcao-cientifica', 'fantasia', 'distopia', 'utopia', 'historia-alternativa'): return 2
        if has('espiritismo', 'espiritualidade'): return 15
        if has('BR', 'RS', 'latam', 'portugal'): return 4
        if has('romance-historico', 'medieval', 'roma', 'antiguidade', 'renascimento'): return 6
        if has('religiao'): return 15
        if has('misterio', 'thriller', 'thriller-medico', 'gotico'): return 7
        if has('psicologia', 'psicanalise'): return 14
        if has('filosofia') and has('introducao'): return 9
        if has('classico', 'existencialismo', 'etica', 'filosofia'): return 3
        return 5
    # não ficção (ou sem tipo)
    if has('espiritismo', 'umbanda', 'oriental', 'mistica', 'espiritualidade'): return 15
    if has('parentalidade', 'escrita', 'cinema', 'arte'): return 16
    if has('neurociencia', 'consciencia'): return 10
    if has('psicologia', 'psicanalise', 'psiquiatria'): return 14
    if has('filosofia', 'existencialismo', 'etica'): return 9
    if has('ia', 'ciencia', 'medicina'): return 13
    if has('historia', 'antropologia', 'sociologia', 'testemunho', 'esporte'): return 12
    if has('politica', 'autoritarismo', 'economia', 'geopolitica', 'gestao'): return 11
    return 12
