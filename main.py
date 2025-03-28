import random

# Parametri delle squadre
squadra_A = {'nome': 'Squadra A', 'attacco': 70, 'difesa': 60}
squadra_B = {'nome': 'Squadra B', 'attacco': 65, 'difesa': 65}

# Condizioni virtuali
meteo = {'sole': 1.0, 'pioggia': 0.8, 'neve': 0.6}  # Fattore di influenza sul numero di gol

# Funzione per simulare una partita
def simula_partita(squadra_A, squadra_B, meteo_corrente):
    # Fattore casuale per rendere il risultato imprevedibile
    fattore_casuale_A = random.uniform(0.5, 1.5)
    fattore_casuale_B = random.uniform(0.5, 1.5)
    
    # Calcolo dei gol segnati da ciascuna squadra
    gol_A = (squadra_A['attacco'] / squadra_B['difesa']) * fattore_casuale_A * meteo[meteo_corrente]
    gol_B = (squadra_B['attacco'] / squadra_A['difesa']) * fattore_casuale_B * meteo[meteo_corrente]
    
    # Arrotondamento dei gol
    gol_A = round(gol_A)# Arrotondiamo e assicuriamoci che non sia negativo
    gol_B = round(gol_B) 
    
    return gol_A, gol_B

# Funzione per simulare N partite e calcolare le probabilità
def calcola_quote(squadra_A, squadra_B, meteo_corrente, num_simulazioni=10000):
    vittorie_A = 0
    vittorie_B = 0
    pareggi = 0
    
    for _ in range(num_simulazioni):
        gol_A, gol_B = simula_partita(squadra_A, squadra_B, meteo_corrente)
        
        if gol_A > gol_B:
            vittorie_A += 1
        elif gol_B > gol_A:
            vittorie_B += 1
        else:
            pareggi += 1
    
    # Calcolo delle probabilità
    prob_A = vittorie_A / num_simulazioni
    prob_B = vittorie_B / num_simulazioni
    prob_pareggio = pareggi / num_simulazioni
    
    # Conversione in quote decimali
    quota_A = 1 / prob_A if prob_A > 0 else 0
    quota_B = 1 / prob_B if prob_B > 0 else 0
    quota_pareggio = 1 / prob_pareggio if prob_pareggio > 0 else 0
    
    return quota_A, quota_B, quota_pareggio

# Esempio di utilizzo
meteo_corrente = 'sole'  # Cambia il meteo per vedere come influisce sulle quote
quota_A, quota_B, quota_pareggio = calcola_quote(squadra_A, squadra_B, meteo_corrente)

print(f"Quote per {squadra_A['nome']}: {quota_A:.2f}")
print(f"Quote per {squadra_B['nome']}: {quota_B:.2f}")
print(f"Quote per il pareggio: {quota_pareggio:.2f}")
