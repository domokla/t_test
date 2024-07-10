
import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Munkakönyvtár beállítása és fájl beolvasása
os.chdir("/Users/domokla/Library/Mobile Documents/com~apple~CloudDocs/PHD/PTSD/ugur")
file = 'adat.xlsx'
df = pd.read_excel(file, sheet_name='Sheet1')

def analyse_data(output, df, szures, adat, description):
    with open(output, 'w') as f:
        # Leírás kiírása a fájl elejére
        f.write(description + '\n')
        
        # Szűrések
        both_positive = df[(df['gper1'] == 'positive') & (df['kol17'] == 'positive')][adat].dropna()
        one_positive = df[szures][adat].dropna()
        
        # Ellenőrizzük, hogy a minták nem üresek-e
        if both_positive.empty or one_positive.empty:
            f.write("Hiba: Az egyik vagy mindkét minta üres.\n")
            return
        
        # Normális eloszlás vizsgálata Shapiro-Wilk teszttel
        shapiro_both_positive = stats.shapiro(both_positive)
        shapiro_one_positive = stats.shapiro(one_positive)
    
        # Eredmények kiírása
        f.write(f"Shapiro-Wilk teszt (Both Positive): p-érték = {shapiro_both_positive.pvalue}\n")
        if shapiro_both_positive.pvalue < 0.05:
            f.write("Both Positive minta nem normális eloszlású.\n")
        else:
            f.write("Both Positive minta normális eloszlású.\n")
    
        f.write(f"Shapiro-Wilk teszt (One Positive): p-érték = {shapiro_one_positive.pvalue}\n")
        if shapiro_one_positive.pvalue < 0.05:
            f.write("One Positive minta nem normális eloszlású.\n")
        else:
            f.write("One Positive minta normális eloszlású.\n")
    
        # Hisztogramok készítése az eloszlások vizsgálatához
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(both_positive, bins=10, alpha=0.7, label='Both Positive')
        plt.title('Histogram of Breslow Thickness (Both Positive)')
        plt.xlabel('Breslow Thickness')
        plt.ylabel('Frequency')
        plt.legend()
    
        plt.subplot(1, 2, 2)
        plt.hist(one_positive, bins=10, alpha=0.7, label='One Positive')
        plt.title('Histogram of Breslow Thickness (One Positive)')
        plt.xlabel('Breslow Thickness')
        plt.ylabel('Frequency')
        plt.legend()
    
        plt.tight_layout()
        plt.show()
    
        # Levene-teszt a varianciák egyenlőségének ellenőrzésére
        levene_test = stats.levene(both_positive, one_positive)
        f.write(f"Levene-teszt: p-érték = {levene_test.pvalue}\n")
        if levene_test.pvalue < 0.05:
            f.write("A varianciák nem egyenlők.\n")
        else:
            f.write("A varianciák egyenlők.\n")
    
        # Ha az eloszlás nem normális, vagy a varianciák nem egyenlők, Mann-Whitney U tesztet használunk
        if shapiro_both_positive.pvalue < 0.05 or shapiro_one_positive.pvalue < 0.05 or levene_test.pvalue < 0.05:
            u_stat, u_p_value = stats.mannwhitneyu(both_positive, one_positive)
            f.write(f"Mann-Whitney U teszt: U-statisztika = {u_stat}, p-érték = {u_p_value}\n")
            if u_p_value < 0.05:
                f.write("Az átlagok szignifikánsan eltérnek (Mann-Whitney U teszt).\n")
            else:
                f.write("Az átlagok nem térnek el szignifikánsan (Mann-Whitney U teszt).\n")
        else:
            t_statistic, p_value = stats.ttest_ind(both_positive, one_positive, alternative='two-sided')
            f.write(f"T-statistic: {t_statistic}\n")
            f.write(f"P-value: {p_value}\n")
            if p_value < 0.05:
                f.write("Az átlagok szignifikánsan eltérnek (t-teszt).\n")
            else:
                f.write("Az átlagok nem térnek el szignifikánsan (t-teszt).\n")

analyse_data('kol17_breslow_pos.txt', df, (df['gper1'] == 'negative') & (df['kol17'] == 'positive'), 'breslow','GPER1 = negative, KOL17 = positive összehasonlítas a dupla pozitívval')
analyse_data('gper1_breslow_pos.txt', df, (df['gper1'] == 'positive') & (df['kol17'] == 'negative'), 'breslow', 'GPER1 = positive, KOL17 = negative összehasonlítas a dupla pozitívval')

analyse_data('kol17_mitozis_pos.txt', df, (df['gper1'] == 'negative') & (df['kol17'] == 'positive'), 'mitozis','GPER1 = negative, KOL17 = positive összehasonlítas a dupla pozitívval')
analyse_data('gper1_mitozis_pos.txt', df, (df['gper1'] == 'positive') & (df['kol17'] == 'negative'), 'mitozis', 'GPER1 = positive, KOL17 = negative összehasonlítas a dupla pozitívval')





