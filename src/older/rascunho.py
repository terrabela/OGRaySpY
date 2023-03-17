# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 18:35:29 2017

@author: mmaduar
"""


#########################

if platform.startswith('linux'):
    flocalprefix = r'/home/marcelo/wolkesicher/ipen/Genie2k/Camfiles/Pni/2012_Ago/'
else:
    if node() == 'mmaduar-net3':
        flocalprefix = r'/Users/mmaduar/wolkesicher/Python_Scripts/OpenGRay/spyd1/'
    else:
        flocalprefix = r'/Users/Marcelo/wolkesicher/Python_Scripts/OpenGRay/spyd1/'
    
# flocalname = flocalprefix + 'lran12910.iec'
# flocalname = flocalprefix + 'ctp1404.iec'
flocalname = flocalprefix + 'ctp1508.iec'

fi = open(flocalname, 'r')

lins = fi.readlines()
fi.close()

inidat = 1
for lin in lins:
    if lin.find(r'A004USERDEFINED') == 0:
        break
    inidat += 1
    
cnts = []
itr = list(range( inidat, len(lins) ))
for ilin in itr:
    cnts.append( int(lins[ilin][10:20]) )
    cnts.append( int(lins[ilin][20:30]) )
    cnts.append( int(lins[ilin][30:40]) )
    cnts.append( int(lins[ilin][40:50]) )
    cnts.append( int(lins[ilin][50:60]) )
del itr
del lins

###############################################




           if self.docum.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                # 2017-04-29 Create db for this spectrum
                # 2017-07-19 RETOMAR!!
                # self.uiuiui = SpectrumDb(fileName + '.db')
                self.parsed.readiecsp( fileName )
                print( self.parsed.lt )

                self.parsed.analyzeiecsp()

                self.sc.plotnewdata(self.parsed.nonull_chan, self.parsed.nonull_cnts,
                                    self.parsed.nonull_unct )

                print(self.parsed.regions, self.parsed.xforplot, self.parsed.bl_forplot, self.parsed.net_forplot)


                self.scPlot2.plotwstd( self.parsed.wstd )
                self.sc.plotRegionsFit( self.parsed.regions, self.parsed.zrg )
                self.sc.plotBaselinesFit( self.parsed.zbl, self.parsed.blin )
                # self.sc.plotOtherStuff( self.parsed.regions, self.parsed.xforplot,
                #                       self.parsed.bl_forplot, self.parsed.net_forplot)


        # + str( self.spMCA))
        #+ str(self.spSegm)+ str( self.spStartSec1))
        #+
        #                 str(self.spStartSec2 )+ str(self.spRLTime20ms)+
        #                str(self.spLVTime20ms)+ str(self.spdd1 )+str(self.spdd2 )+
        #               str(self.spMM1 )+str(self.spMM2 )+str(self.spMM3 )+
        #              str(self.spyy1 )+str(self.spyy2 )+ str(self.spsep )+
        #             str(self.sphh1 )+ str(self.sphh2 )+ str(self.spmm1 )+
        #            str(self.spmm2 )+ str(self.spChOffset )+str(self.spLngData  )
               #           )
        

#bool SpectrumIO::loadSpectrumCHN(const QString &fileName)
#{
#    m_filename = fileName;
#    QFile file(fileName);
#    if (!file.open(QFile::ReadOnly)) return false;
#    inDst = new QDataStream(&file);
#    inDst->setByteOrder( QDataStream::LittleEndian );
#    if (!getHeaderCHN()) return false;
#    if (!getCountsCHN()) return false;
#    if (!getFooterCHN()) return false;
#    return true;
#}


#QDateTime SpectrumIO::toDateTimeCentury(const QString &s)
#{
#    // 2-digit year specifications will be interpreted as years between 1980 and 2079.
#    QString sloc = s;
#    int yy = s.mid(6, 2).toInt();
#    if ( yy < 80 )
#        sloc.insert( 6, "20" );
#    else
#        sloc.insert( 6, "19" );
#    return QDateTime::fromString( sloc, "dd/MM/yyyy hh:mm:ss" );
#}
        