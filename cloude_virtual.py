import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class GeneratoreQuoteCalcioVirtuale:
    def __init__(self, margine_operatore=0.10):
        """
        Inizializza il generatore di quote per partite di calcio con un margine operatore predefinito
        
        :param margine_operatore: percentuale di margine che l'operatore vuole mantenere (0.10 = 10%)
        """
        self.margine_operatore = margine_operatore
        self.squadre_virtuali = self._crea_squadre_virtuali()
        
    def _crea_squadre_virtuali(self, num_squadre=20):
        """
        Crea un database di squadre virtuali con forza relativa
        
        :param num_squadre: numero di squadre nel campionato virtuale
        :return: DataFrame con le squadre e le loro caratteristiche
        """
        nomi_squadre = [f"Squadra {chr(65+i)}" for i in range(num_squadre)]
        
        # Forza attacco e difesa su una scala 1-100
        attacco = np.random.randint(50, 95, num_squadre)
        difesa = np.random.randint(50, 95, num_squadre)
        
        # Forma recente (variabile nel tempo)
        forma = np.random.randint(70, 100, num_squadre)
        
        # Fattore campo (vantaggio quando gioca in casa)
        #fattore_campo = np.random.uniform(1.1, 1.4, num_squadre)
        
        return pd.DataFrame({
            'nome': nomi_squadre,
            'attacco': attacco,
            'difesa': difesa,
            'forma': forma,
            #'fattore_campo': fattore_campo
        })
    
    #non usata
    def aggiorna_forma_squadre(self):
        """
        Aggiorna la forma delle squadre per simulare variazioni nel tempo
        """
        for i in range(len(self.squadre_virtuali)):
            # Varia la forma di ±5 punti
            variazione = random.randint(-5, 5)
            nuova_forma = self.squadre_virtuali.at[i, 'forma'] + variazione
            # Mantieni la forma entro limiti ragionevoli
            self.squadre_virtuali.at[i, 'forma'] = max(min(nuova_forma, 100), 60)
    
    def calcola_probabilita_risultati(self, id_casa, id_trasferta):
        """
        Calcola le probabilità dei tre possibili risultati: 1 (vittoria casa), X (pareggio), 2 (vittoria trasferta)
        
        :param id_casa: indice della squadra di casa
        :param id_trasferta: indice della squadra in trasferta
        :return: dizionario con probabilità 1X2
        """
        # Recupera caratteristiche delle squadre
        squadra_casa = self.squadre_virtuali.iloc[id_casa]
        squadra_trasferta = self.squadre_virtuali.iloc[id_trasferta]
        
        # Calcola forza relativa considerando attacco, difesa, forma e fattore campo
        # Queste quote decidono quanto pesano le statistiche di una squadra
        forza_casa = squadra_casa['attacco'] * 0.4 + squadra_casa['difesa'] * 0.3 + squadra_casa['forma'] * 0.3
        #forza_casa *= squadra_casa['fattore_campo']  # Vantaggio del fattore campo
        
        forza_trasferta = squadra_trasferta['attacco'] * 0.4 + squadra_trasferta['difesa'] * 0.3 + \
                      squadra_trasferta['forma'] * 0.3
        
        # Calcola la differenza di forza
        diff_forza = forza_casa - forza_trasferta
        
        # Calcola probabilità base 1X2 basate sulla differenza di forza
        # Usa una funzione sigmoidale per mappare la differenza di forza a probabilità
        # In base alla differenza di forza delle squadre assegna le percentuali ai risultati, utilizzando una funzione sigmoidale

        """
        Se diff_forza = 0 (squadre perfettamente equilibrate):

        prob_1 = 1 / (1 + e^0) * 0.7 = 0.5 * 0.7 = 0.35 (35%)
        prob_2 = 1 / (1 + e^0) * 0.7 = 0.5 * 0.7 = 0.35 (35%)
        prob_x = 1 - (0.35 + 0.35) = 0.3 (30%)

        Se diff_forza = 30 (squadra di casa notevolmente più forte):

        prob_1 = 1 / (1 + e^-1) * 0.7 ≈ 0.73 * 0.7 ≈ 0.51 (51%)
        prob_2 = 1 / (1 + e^1) * 0.7 ≈ 0.27 * 0.7 ≈ 0.19 (19%)
        prob_x = 1 - (0.51 + 0.19) = 0.3 (30%)

        Se diff_forza = 60 (squadra di casa estremamente più forte):

        prob_1 = 1 / (1 + e^-2) * 0.7 ≈ 0.88 * 0.7 ≈ 0.62 (62%)
        prob_2 = 1 / (1 + e^2) * 0.7 ≈ 0.12 * 0.7 ≈ 0.08 (8%)
        prob_x = 1 - (0.62 + 0.08) = 0.3 (30%)
        
        """

        prob_1 = 1 / (1 + np.exp(-diff_forza/30)) * 0.7  # Limita max probabilità a circa 70%
        prob_2 = 1 / (1 + np.exp(diff_forza/30)) * 0.7

        # Il pareggio ha una probabilità base più alta nel calcio (circa 25-30%)
        # Calcolo il pareggio come complementare della somma delle altre probabilità
        prob_x = 1 - (prob_1 + prob_2)
        
        # Aggiungi una piccola variazione casuale, utilizzando una distribuzione uniforme
        """
        Una distribuzione uniforme in statistica ha queste proprietà chiave:

        Equi-probabilità: Tutti i valori nell'intervallo specificato hanno esattamente la stessa probabilità di essere selezionati.
        Range definito: La distribuzione è limitata da un valore minimo e massimo (nel nostro caso, -0.05 e +0.05).
        Densità di probabilità costante: Se disegnassimo un grafico della funzione di densità di probabilità, sarebbe una linea orizzontale nell'intervallo specificato.
        
        """
        variazione = 0.05
        prob_1 = prob_1 * (1 + random.uniform(-variazione, variazione))
        prob_2 = prob_2 * (1 + random.uniform(-variazione, variazione))
        prob_x = prob_x * (1 + random.uniform(-variazione, variazione))
        
        # Normalizza per assicurarsi che la somma sia 1
        totale = prob_1 + prob_x + prob_2
        prob_1 /= totale
        prob_x /= totale
        prob_2 /= totale
        
        return {
            '1': prob_1,  # Vittoria casa
            'X': prob_x,  # Pareggio
            '2': prob_2   # Vittoria trasferta
        }
    
    def calcola_quote_1x2(self, probabilita):
        """
        Converte le probabilità in quote con l'aggiunta del margine operatore
        
        :param probabilita: dizionario con probabilità 1X2
        :return: dizionario con quote 1X2
        """
        quote = {}
        for risultato, prob in probabilita.items():
            # Aggiungi il margine dell'operatore
            prob_con_margine = prob / (1 + self.margine_operatore)
            # Converti in quota europea (1/p) e arrotonda a 2 decimali
            quote[risultato] = round(1 / prob_con_margine, 2)
        
        return quote
    
    def calcola_quote_under_over(self, id_casa, id_trasferta):
        """
        Calcola le quote per Under/Over 2.5 gol
        
        :param id_casa: indice della squadra di casa
        :param id_trasferta: indice della squadra in trasferta
        :return: dizionario con quote Under/Over
        """
        # Recupera caratteristiche delle squadre
        squadra_casa = self.squadre_virtuali.iloc[id_casa]
        squadra_trasferta = self.squadre_virtuali.iloc[id_trasferta]
        
        # Potenziale offensivo combinato (più alto = più gol probabili)
        potenziale_offensivo = (squadra_casa['attacco'] + squadra_trasferta['attacco']) / 200
        
        # Potenziale difensivo combinato (più alto = meno gol probabili)
        potenziale_difensivo = (squadra_casa['difesa'] + squadra_trasferta['difesa']) / 200
        
        # Probabilità base dell'Over 2.5
        # 1 - potenziale_difensivo -> debolezza difensiva
        # Prob di fare gol
        prob_over = potenziale_offensivo * 0.6 + (1 - potenziale_difensivo) * 0.4
        
        # Aggiungi variazione casuale
        prob_over = prob_over * (1 + random.uniform(-0.1, 0.1))
        
        # Limita la probabilità in un range realistico (35-75%)
        prob_over = max(min(prob_over, 0.75), 0.35)
        
        # Probabilità Under = 1 - Probabilità Over
        prob_under = 1 - prob_over
        
        # Aggiungi il margine e converti in quote
        prob_over_con_margine = prob_over / (1 + self.margine_operatore)
        prob_under_con_margine = prob_under / (1 + self.margine_operatore)
        
        return {
            'Under 2.5': round(1 / prob_under_con_margine, 2),
            'Over 2.5': round(1 / prob_over_con_margine, 2)
        }
    
    def calcola_quote_goal_nogoal(self, id_casa, id_trasferta):
        """
        Calcola le quote per Goal/NoGoal
        
        :param id_casa: indice della squadra di casa
        :param id_trasferta: indice della squadra in trasferta
        :return: dizionario con quote Goal/NoGoal
        """
        # Recupera caratteristiche delle squadre
        squadra_casa = self.squadre_virtuali.iloc[id_casa]
        squadra_trasferta = self.squadre_virtuali.iloc[id_trasferta]
        
        # Potenziale offensivo di entrambe le squadre
        off_casa = squadra_casa['attacco'] / 100
        off_trasferta = squadra_trasferta['attacco'] / 100
        
        # Potenziale difensivo di entrambe le squadre
        dif_casa = squadra_casa['difesa'] / 100
        dif_trasferta = squadra_trasferta['difesa'] / 100
        
        # Probabilità che entrambe le squadre segnino
        prob_goal = off_casa * (1 - dif_trasferta) * 0.8 + off_trasferta * (1 - dif_casa) * 0.8
        
        # Limita la probabilità in un range realistico (40-75%)
        prob_goal = max(min(prob_goal, 0.75), 0.4)
        
        # Aggiungi variazione casuale
        prob_goal = prob_goal * (1 + random.uniform(-0.05, 0.05))
        
        # Probabilità NoGoal = 1 - Probabilità Goal
        prob_nogoal = 1 - prob_goal
        
        # Aggiungi il margine e converti in quote
        prob_goal_con_margine = prob_goal / (1 + self.margine_operatore)
        prob_nogoal_con_margine = prob_nogoal / (1 + self.margine_operatore)
        
        return {
            'Goal': round(1 / prob_goal_con_margine, 2),
            'NoGoal': round(1 / prob_nogoal_con_margine, 2)
        }
    
    def simula_partita(self, id_casa, id_trasferta):
        """
        Simula il risultato di una partita
        
        :param id_casa: indice della squadra di casa
        :param id_trasferta: indice della squadra in trasferta
        :return: tuple (gol_casa, gol_trasferta)
        """
        # Recupera caratteristiche delle squadre
        squadra_casa = self.squadre_virtuali.iloc[id_casa]
        squadra_trasferta = self.squadre_virtuali.iloc[id_trasferta]
        
        # Calcola potenziale offensivo contro difensivo
        off_vs_dif_casa = squadra_casa['attacco'] / squadra_trasferta['difesa'] 
        #* squadra_casa['fattore_campo']
        off_vs_dif_trasferta = squadra_trasferta['attacco'] / squadra_casa['difesa']
        
        # Aggiungi effetto della forma
        off_vs_dif_casa *= (squadra_casa['forma'] / 85)
        off_vs_dif_trasferta *= (squadra_trasferta['forma'] / 85)
        
        # Calcola la media di gol attesi (usando distribuzione di Poisson)
        media_gol_casa = off_vs_dif_casa * 1.4  # Media storica di gol in casa è circa 1.4
        media_gol_trasferta = off_vs_dif_trasferta * 1.1  # Media storica di gol in trasferta è circa 1.1
        
        # Simula i gol usando una distribuzione di Poisson
        gol_casa = np.random.poisson(media_gol_casa)
        gol_trasferta = np.random.poisson(media_gol_trasferta)
        
        return (gol_casa, gol_trasferta)
    
    def genera_calendario_virtuale(self, num_partite=10):
        """
        Genera un calendario di partite virtuali
        
        :param num_partite: numero di partite da generare
        :return: DataFrame con il calendario delle partite
        """
        num_squadre = len(self.squadre_virtuali)
        partite = []
        
        ora_base = datetime.now()
        
        for i in range(num_partite):
            # Seleziona due squadre diverse casualmente
            id_casa = random.randint(0, num_squadre-1)
            id_trasferta = random.randint(0, num_squadre-1)
            while id_casa == id_trasferta:
                id_trasferta = random.randint(0, num_squadre-1)
            
            # Calcola quote per diversi mercati
            probabilita_1x2 = self.calcola_probabilita_risultati(id_casa, id_trasferta)
            quote_1x2 = self.calcola_quote_1x2(probabilita_1x2)
            quote_under_over = self.calcola_quote_under_over(id_casa, id_trasferta)
            quote_goal_nogoal = self.calcola_quote_goal_nogoal(id_casa, id_trasferta)
            
            # Orario della partita (ogni 3 minuti per le scommesse virtuali)
            orario = ora_base + timedelta(minutes=3*i)
            
            partita = {
                'id': i+1,
                'data_ora': orario,
                'squadra_casa': self.squadre_virtuali.at[id_casa, 'nome'],
                'squadra_trasferta': self.squadre_virtuali.at[id_trasferta, 'nome'],
                'id_casa': id_casa,
                'id_trasferta': id_trasferta,
                'quota_1': quote_1x2['1'],
                'quota_X': quote_1x2['X'],
                'quota_2': quote_1x2['2'],
                'quota_under': quote_under_over['Under 2.5'],
                'quota_over': quote_under_over['Over 2.5'],
                'quota_goal': quote_goal_nogoal['Goal'],
                'quota_nogoal': quote_goal_nogoal['NoGoal']
            }
            
            partite.append(partita)
        
        return pd.DataFrame(partite)
    
    def simula_giornata_completa(self, calendario):
        """
        Simula i risultati di tutte le partite in calendario
        
        :param calendario: DataFrame con il calendario delle partite
        :return: DataFrame con calendario e risultati
        """
        risultati = calendario.copy()
        
        for index, partita in calendario.iterrows():
            # Simula il risultato
            gol_casa, gol_trasferta = self.simula_partita(partita['id_casa'], partita['id_trasferta'])
            
            # Aggiungi risultato
            risultati.at[index, 'gol_casa'] = gol_casa
            risultati.at[index, 'gol_trasferta'] = gol_trasferta
            
            # Determina risultato 1X2
            if gol_casa > gol_trasferta:
                risultati.at[index, 'risultato'] = '1'
            elif gol_casa == gol_trasferta:
                risultati.at[index, 'risultato'] = 'X'
            else:
                risultati.at[index, 'risultato'] = '2'
            
            # Determina Under/Over 2.5
            risultati.at[index, 'under_over'] = 'Over 2.5' if (gol_casa + gol_trasferta) > 2.5 else 'Under 2.5'
            
            # Determina Goal/NoGoal
            risultati.at[index, 'goal_nogoal'] = 'Goal' if (gol_casa > 0 and gol_trasferta > 0) else 'NoGoal'
        
        return risultati


# Esempio d'uso
if __name__ == "__main__":
    # Crea un generatore con 10% di margine
    generatore = GeneratoreQuoteCalcioVirtuale(margine_operatore=0.10)
    
    # Mostra informazioni sulle squadre
    print("CAMPIONATO VIRTUALE - SQUADRE:")
    print(generatore.squadre_virtuali[['nome', 'attacco', 'difesa', 'forma']])
    print("\n")
    
    # Genera un calendario di partite virtuali
    calendario = generatore.genera_calendario_virtuale(num_partite=5)
    
    print("CALENDARIO PARTITE VIRTUALI:")
    print(calendario[['id', 'data_ora', 'squadra_casa', 'squadra_trasferta', 
                     'quota_1', 'quota_X', 'quota_2']].to_string(index=False))
    print("\n")
    
    # Mostra quote aggiuntive per la prima partita
    print(f"QUOTE DETTAGLIATE - {calendario.at[0, 'squadra_casa']} vs {calendario.at[0, 'squadra_trasferta']}:")
    print(f"1X2: 1={calendario.at[0, 'quota_1']}, X={calendario.at[0, 'quota_X']}, 2={calendario.at[0, 'quota_2']}")
    print(f"Under/Over 2.5: Under={calendario.at[0, 'quota_under']}, Over={calendario.at[0, 'quota_over']}")
    print(f"Goal/NoGoal: Goal={calendario.at[0, 'quota_goal']}, NoGoal={calendario.at[0, 'quota_nogoal']}")
    print("\n")
    
    # Simula i risultati
    risultati = generatore.simula_giornata_completa(calendario)
    
    print("RISULTATI SIMULATI:")
    print(risultati[['id', 'squadra_casa', 'squadra_trasferta', 'gol_casa', 'gol_trasferta', 
                    'risultato', 'under_over', 'goal_nogoal']].to_string(index=False))
    print("\n")
    
    # Calcola payout percentuale medio
    payout_1x2 = 1 / ((1/risultati['quota_1']) + (1/risultati['quota_X']) + (1/risultati['quota_2']))
    payout_medio = payout_1x2.mean()
    print(f"Payout percentuale medio (1X2): {payout_medio*100:.2f}%")
    print(f"Margine operatore: {generatore.margine_operatore*100:.2f}%")