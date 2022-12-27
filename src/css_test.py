import pandas as pd
import numpy as np

# 2022-12_27
# Adapted from
# https://stackoverflow.com/questions/50807744/apply-css-class-to-pandas-dataframe-using-to-html#50939211

pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')


def css_test():
    np.random.seed(6182018)
    demo_df = pd.DataFrame({'date': np.random.choice(pd.date_range('2018-01-01', '2018-06-18', freq='D'), 50),
                            'analysis_tool': np.random.choice(['pandas', 'r', 'julia', 'sas', 'stata', 'spss'], 50),
                            'database': np.random.choice(['postgres', 'mysql', 'sqlite', 'oracle', 'sql server', 'db2'],
                                                         50),
                            'os': np.random.choice(
                                ['windows 10', 'ubuntu', 'mac os', 'android', 'ios', 'windows 7', 'debian'], 50),
                            'num1': np.random.randn(50) * 100,
                            'num2': np.random.uniform(0, 1, 50),
                            'num3': np.random.randint(100, size=50),
                            'bool': np.random.choice([True, False], 50)
                            },
                           columns=['date', 'analysis_tool', 'num1', 'database', 'num2', 'os', 'num3', 'bool']
                           )

    print(demo_df.head(10))
    #      date    analysis_tool     num1      database     num2        os      num3  bool
    # 0 2018-04-21     pandas     153.474246       mysql  0.658533         ios   74    True
    # 1 2018-04-13        sas     199.461669      sqlite  0.656985   windows 7   11   False
    # 2 2018-06-09      stata      12.918608      oracle  0.495707     android   25   False
    # 3 2018-04-24       spss      88.562111  sql server  0.113580   windows 7   42   False
    # 4 2018-05-05       spss     110.231277      oracle  0.660977  windows 10   76    True
    # 5 2018-04-05        sas     -68.140295  sql server  0.346894  windows 10    0    True
    # 6 2018-05-07      julia      12.874660    postgres  0.195217         ios   79    True
    # 7 2018-01-22          r     189.410928       mysql  0.234815  windows 10   56   False
    # 8 2018-01-12     pandas    -111.412564  sql server  0.580253      debian   30   False
    # 9 2018-04-12          r      38.963967    postgres  0.266604   windows 7   46   False

    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>

    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''

    # OUTPUT AN HTML FILE
    with open('my_file.html', 'w') as f:
        f.write(html_string.format(table=demo_df.to_html(classes='mystyle')))


def apply_css(report_df):
    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>

    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {report_header}
        {table}
        {footer}
      </body>
    </html>.
    '''

    report_header = '<p>Este é o cabeçalho do relatório</p>'
    footer = '''
    <p>(*) Intervalo de confiança: ± 1 &sigma; (68%)</p>
    <p>Técnica analítica utilizada: espectrometria gama passiva</p>
    <p>Data e horário de início da medida: 04/08/2022, 19h42</p>
    <p>Intervalo de tempo de medida: 50 000 s</p>
    <p>Observações:</p>
    <p>1. Os resultados relacionados foram corrigidos para a data e
    horário de desligamento do Reator IEA-R1.</p>
    <p>2. A representatividade da amostra, bem como outras informações
    fornecidas que não sejam diretamente relacionadas ao conteúdo de
    radioatividade, são de responsabilidade exclusiva do solicitante.</p>
    <p>Dr. Marcelo Francis Máduar</p>
    <p>Serviço de Gestão de Radiometria Ambiental</p>
    <p>Instituto de Pesquisas Energéticas e Nucleares</p>
    <p>Centro de Metrologia das Radiações Ionizantes</p>
    <p>Av. Prof. Lineu Prestes, 2242 - Cidade Universitária - CEP 05508-000</p>
    <p>Tel: (11) 2810 5017</p>
    <p>São Paulo - Estado de São Paulo</p>
    <p>e-mail: mmaduar@ipen.br</p>
    '''

    # OUTPUT AN HTML FILE
    with open('an_html_file.html', 'w') as f:
        f.write(html_string.format(
            report_header=report_header,
            table=report_df.to_html(classes='mystyle'),
            footer=footer
        ))
