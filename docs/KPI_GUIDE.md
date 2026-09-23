# Guide til KPI'er og grafer

Dashboardet viser fire bank-KPI'er og seks KPI'er for skadesforsikring. Sammenlign kun selskaber inden for samme marked, og se altid på år, datadækning og forretningsmodel før du konkluderer noget ud fra én værdi.

## Hvad betyder retning?

- **Højere er som udgangspunkt bedre:** En større værdi peger normalt på stærkere indtjening eller afkast. Det er ikke en garanti for lavere risiko.
- **Lavere er som udgangspunkt bedre:** En mindre andel af præmier eller indtjening går normalt til erstatninger eller omkostninger. Forskelle i produkter, reserver og genforsikring kan ændre sammenligningen.
- **Neutral:** Tallet beskriver størrelse eller udvikling, men hverken højere eller lavere er entydigt bedst. Dashboardet viser derfor ingen præstationspercentil for disse KPI'er.

En negativ KPI-værdi betyder ikke altid det samme. Negativ egenkapitalforrentning viser underskud, mens negativt relativt afløbsresultat peger på ugunstig udvikling i tidligere skadehensættelser. For neutrale KPI'er vurderes fortegnet sammen med årsagen og udviklingen over flere år.

## Bank

| KPI | Definition og læsning | Retning |
| --- | --- | --- |
| Indtjening pr. omkostningskrone | De medtagne indtægter divideret med de medtagne omkostninger. 1,50x er 1,50 kr. indtjening pr. 1,00 kr. omkostning. Over 1,00x dækker indtægterne de medtagne omkostninger; engangsindtægter kan dog løfte forholdstallet. | Højere er normalt bedre. |
| Egenkapitalforrentning før skat | Resultat før skat divideret med gennemsnitlig egenkapital ved årets begyndelse og slutning. 10 % er 10 kr. resultat før skat pr. 100 kr. egenkapital. Negativ værdi betyder underskud før skat. | Højere er normalt bedre, når risiko og kapitalisering er sammenlignelige. |
| Egenkapitalforrentning efter skat | Resultat efter skat divideret med gennemsnitlig egenkapital. 10 % er 10 kr. resultat efter skat pr. 100 kr. egenkapital. Negativ værdi betyder underskud efter skat. | Højere er normalt bedre, når risiko og kapitalisering er sammenlignelige. |
| Udlån i forhold til egenkapital | Samlede udlån divideret med egenkapital. 5,00x er 5 kr. udlån pr. 1 kr. egenkapital. Høj værdi kan både afspejle mere aktivitet og mere gearing. | Neutral; der er ingen universel god grænse. |

Bank-KPI'erne beregnes fra råregnskabets kontofelter. Se **KPI-definition** på den enkelte side for de præcise felter og forbehold. Manglende input erstattes ikke med nul.

## Forsikring

Definitionerne følger den leverede `Finanstilsynet_noegletal_master.xlsx` og [reglerne om femårsoversigt for skadesforsikringsselskaber, bilag 10](https://www.retsinformation.dk/api/pdf/249994). Dashboardet viser rapporterede selskabsværdier fra det medfølgende KPI-datasæt. Disse værdier genberegnes ikke fra råregnskabets kontokoder.

| KPI | Definition og læsning | Retning |
| --- | --- | --- |
| Bruttoerstatningsprocent | Bruttoerstatningsudgifter divideret med bruttopræmieindtægter efter bonus og præmierabatter. 70 % betyder 70 kr. erstatninger pr. 100 kr. præmier før genforsikring. Over 100 % overstiger erstatningerne alene præmierne. | Lavere er normalt bedre. |
| Bruttoomkostningsprocent | Forsikringsmæssige driftsomkostninger divideret med bruttopræmieindtægter efter bonus og præmierabatter. 17 % betyder 17 kr. drift pr. 100 kr. præmier. Det officielle omkostningsbegreb omfatter en justering for domicilejendomme. | Lavere er normalt bedre. |
| Combined ratio | Summen af erstatningsprocent, omkostningsprocent og nettogenforsikringsprocent. 95 % betyder, at disse komponenter svarer til 95 kr. pr. 100 kr. præmier. Under 100 % peger på overskud i forsikringsdriften før investeringsafkast; over 100 % peger på underskud. | Lavere er normalt bedre. |
| Operating ratio | Som combined ratio, men med allokeret investeringsafkast svarende til forsikringsteknisk rente lagt til præmiegrundlaget. 95 % betyder 95 kr. af de samlede komponenter pr. 100 kr. af dette udvidede grundlag. | Lavere er normalt bedre. |
| Relativt afløbsresultat | Afløbsresultat for tidligere års skader divideret med de primohensættelser, det vedrører. Positivt tal kan afspejle, at tidligere reserver oversteg senere omkostninger; negativt tal kan afspejle det modsatte. Begge skal ses i sammenhæng med reservepraksis. | Neutral. |
| Egenkapitalforrentning i procent | Årets resultat divideret med tidsvægtet gennemsnitlig egenkapital. 10 % er 10 kr. resultat pr. 100 kr. egenkapital. Negativ værdi betyder underskud. | Højere er normalt bedre, når risiko og kapitalisering er sammenlignelige. |

Combined ratio er **ikke nødvendigvis summen af de to viste bruttoprocenter**: nettogenforsikringsprocenten indgår også. Masterfilen angiver, at KPI-datasættet endnu ikke er afstemt én til én mod Finanstilsynets offentlige pivottabel.

## Sådan læses graferne

| Visning | Sådan læses den |
| --- | --- |
| KPI-puls på forsiden | Viser medianen for selskaber med en gyldig KPI i det seneste år med data for netop den KPI. Kortene kan derfor have forskellige år og selskabstal. |
| Overblik: fordeling | Den vandrette akse viser KPI-værdier i intervaller. Søjlehøjden er antal selskaber i intervallet, ikke værdien af ét selskab. |
| Overblik: sektorudvikling | Hvert punkt er medianen eller det simple gennemsnit af tilgængelige selskabsværdier i det år. Selskabskredsen kan ændre sig. Enkeltstående store eller små værdier påvirker gennemsnittet mere end medianen. |
| Udforsk | Hver linje er ét selskab. Vandret akse er år; lodret akse er KPI-værdien. Huller betyder manglende data, ikke nul. |
| Selskabsprofil | Den fuldt optrukne linje viser selskabet. Den stiplede linje viser sektormedianen **i selskabets seneste tilgængelige år** og holdes konstant på grafen; den er ikke en separat median for hvert historisk år. |
| Sektorsammenligning | Søjlelængden er den faktiske KPI-værdi i det valgte år. For KPI'er med en gunstig retning viser farve og percentil selskabets **relative** placering blandt selskaber med data det år. Høj percentil er gunstig i den angivne retning, men er ikke en absolut kvalitetsgrænse. Neutrale KPI'er vises uden præstationspercentil. |
| Datakvalitet | Dækning er andelen af repræsenterede selskaber med en gyldig KPI-værdi. Lav dækning begrænser, hvor sikkert man kan læse sektorens median, gennemsnit og udvikling. |

Procenter på graferne er procentværdier: 0,70 i beregningsdata vises som 70 %. Et procentpoint er forskellen mellem eksempelvis 70 % og 71 %; det er ikke en relativ stigning på 1 %.
