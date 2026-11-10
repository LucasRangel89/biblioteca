"""Relógio fixo para os testes: o painel gera os dados de exemplo a partir da data de hoje,
então os números esperados só valem se "hoje" for sempre o mesmo dia (09/11/2026, 10h de Brasília)."""
import datetime
HOJE = datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc)
def fixa(pg, quando=None):
    pg.clock.set_fixed_time(quando or HOJE)
    return pg
