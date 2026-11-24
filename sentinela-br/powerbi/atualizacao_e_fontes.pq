// Power Query (M) · consulta "Atualizacao": grava a data e a hora de cada atualização (horário de Brasília)
let
    Agora = DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -3),
    Fonte = #table(type table [DataHora = datetime], {{DateTimeZone.RemoveZone(Agora)}})
in
    Fonte
