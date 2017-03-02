#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"

const float x_1 = -0.5;
const float x_2 = 0.4;
const float x_3 = 0.7;
const float y_1 = -0.5;
const float y_2 = 0.4;
const float y_3 = 0.7;

const float a_1 = -0.3;
const float a_2 = 0.3; 
const float a_3 = 0.7; 
const float b_1 = -0.3;
const float b_2 = 0.2; 
const float b_3 = 0.6; 

float tHq_MVAto1D_3l_16(float mva_tt, float mva_ttv){
/*
These are sorted roughly in increasing signal yield.
 1 ---------------------
   |  6 |  8 | 13 | 16 |
   |----|----|----|----|
   |  4 | 11 | 15 | 14 |
 0 |----|----|----|----|
   |  2 | 10 | 12 |  9 |
   |----|----|----|----|
   |  1 |  3 |  5 |  7 |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 16;
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 13;
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 6;

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 14;
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 15;
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 11;
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 4;

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 9;
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 12;
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 10;
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 2;

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 7;
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 5;
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_3l_12(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   8 + 11
   6 + 4 + 2
   7 + 5
New bins are:
 1 ---------------------
   |    |    |  9 | 12 |
   |    |  8 |----|----|
   |  2 |    | 11 | 10 |
 0 |    |----|----|----|
   |    |  7 |  6 |  5 | 
   |----|----|----|----|
   |  1 |  3 |    4    |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 12;
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 9;
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 10;
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 11;
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 5;
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 6;
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 7;
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 2;

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_3l_10(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   3 + 4
   6 + 5
New bins are:
 1 ---------------------
   |    |    |  7 | 10 |
   |    |  6 |----|----|
   |  2 |    |  9 |  8 |
 0 |    |----|----|----|
   |    |  5 |    4    | 
   |----|----|----|----|
   |  1 |      3       |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 10;
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 7;
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 8;
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 9;
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 4;
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 4;
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 5;
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 2;

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_2lss_10(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   3 + 4
   6 + 5
New bins are:
 1 ---------------------
   |    |    |  7 | 10 |
   |    |  6 |----|----|
   |  2 |    |  9 |  8 |
 0 |    |----|----|----|
   |    |  5 |    4    | 
   |----|----|----|----|
   |  1 |      3       |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > a_3  && mva_ttv  >  b_3 ) return 10;
    if( mva_tt  > a_2  && mva_ttv  >  b_3 ) return 7;
    if( mva_tt  > a_1  && mva_ttv  >  b_3 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  b_3 ) return 2;

    if( mva_tt  > a_3  && mva_ttv  >  b_2 ) return 8;
    if( mva_tt  > a_2  && mva_ttv  >  b_2 ) return 9;
    if( mva_tt  > a_1  && mva_ttv  >  b_2 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  b_2 ) return 2;

    if( mva_tt  > a_3  && mva_ttv  >  b_1 ) return 4;
    if( mva_tt  > a_2  && mva_ttv  >  b_1 ) return 4;
    if( mva_tt  > a_1  && mva_ttv  >  b_1 ) return 5;
    if( mva_tt >= -1.0 && mva_ttv  >  b_1 ) return 2;

    if( mva_tt  > a_3  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > a_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > a_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_2lss_12(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   6 + 8
   2 + 4
   3 + 5
   7 + 9
New bins are:
 1 ---------------------
   |   10    | 11 | 12 |
   |----|----|----|----|
   |    |  7 |  9 |  8 |
 0 |  2 |----|----|----|
   |    |  6 |  5 |    | 
   |----|----|----|  4 |
   |  1 |    3    |    |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > a_3  && mva_ttv  >  b_3 ) return 12;
    if( mva_tt  > a_2  && mva_ttv  >  b_3 ) return 11;
    if( mva_tt  > a_1  && mva_ttv  >  b_3 ) return 10;
    if( mva_tt >= -1.0 && mva_ttv  >  b_3 ) return 10;

    if( mva_tt  > a_3  && mva_ttv  >  b_2 ) return 9;
    if( mva_tt  > a_2  && mva_ttv  >  b_2 ) return 8;
    if( mva_tt  > a_1  && mva_ttv  >  b_2 ) return 7;
    if( mva_tt >= -1.0 && mva_ttv  >  b_2 ) return 2;

    if( mva_tt  > a_3  && mva_ttv  >  b_1 ) return 4;
    if( mva_tt  > a_2  && mva_ttv  >  b_1 ) return 5;
    if( mva_tt  > a_1  && mva_ttv  >  b_1 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  b_1 ) return 2;

    if( mva_tt  > a_3  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > a_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > a_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;
    return 0;
}

class GetTHQBinning
{
public:
    GetTHQBinning(TString fileName2l="tHq-multilepton/signal_extraction/binning_2l.root",
                  TString fileName3l="tHq-multilepton/signal_extraction/binning_3l.root",
                  TString histname="hTargetBinning");
    Int_t GetCluster2l(Double_t, Double_t);
    Int_t GetCluster3l(Double_t, Double_t);
protected:
    TFile* file2l;
    TFile* file3l;
    TH2F* hBinning2l;
    TH2F* hBinning3l;
};

GetTHQBinning::GetTHQBinning(TString fileName2l, TString fileName3l, TString histname){
    file2l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName2l);
    file3l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName3l);
    if (!file2l || !file2l->IsOpen()) file2l = TFile::Open(fileName2l);
    if (!file3l || !file3l->IsOpen()) file3l = TFile::Open(fileName3l);
    hBinning2l = (TH2F*) file2l->Get(histname);
    hBinning3l = (TH2F*) file3l->Get(histname);
}

Int_t GetTHQBinning::GetCluster2l( Double_t x, Double_t y){
    return hBinning2l->GetBinContent( hBinning2l->FindBin(x,y) );
}

Int_t GetTHQBinning::GetCluster3l( Double_t x, Double_t y){
    return hBinning3l->GetBinContent( hBinning3l->FindBin(x,y) );
}

GetTHQBinning SBRatioClustering;
Int_t tHq_MVAto1D_2lss_sbratio(Double_t x, Double_t y){
    return SBRatioClustering.GetCluster2l(x,y)+1;
}

Int_t tHq_MVAto1D_3l_sbratio(Double_t x, Double_t y){
    return SBRatioClustering.GetCluster3l(x,y)+1;
}

GetTHQBinning KMeansBinning = GetTHQBinning(
                            "tHq-multilepton/signal_extraction/binning_kmeans_2l.root",    // 10 bins
                            "tHq-multilepton/signal_extraction/binning_kmeans_3l_5.root",  // 5 bins
                            "hBinning");
Int_t tHq_MVAto1D_2lss_kmeans(Double_t x, Double_t y){
    return KMeansBinning.GetCluster2l(x,y)+1;
}

Int_t tHq_MVAto1D_3l_kmeans(Double_t x, Double_t y){
    return KMeansBinning.GetCluster3l(x,y)+1;
}


float fwdjet_eventWeight_25(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
Forward jet pt cut of 25 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0662;
  if(eta < 0.556) return 1.0720;
  if(eta < 0.833) return 1.0640;
  if(eta < 1.111) return 1.0695;
  if(eta < 1.389) return 1.0572;
  if(eta < 1.667) return 1.0109;
  if(eta < 1.944) return 1.0537;
  if(eta < 2.222) return 1.0500;
  if(eta < 2.500) return 1.0100;
  if(eta < 2.778) return 1.0526;
  if(eta < 3.056) return 1.0059;
  if(eta < 3.333) return 0.8293;
  if(eta < 3.611) return 0.9290;
  if(eta < 3.889) return 0.8861;
  if(eta < 4.167) return 0.9487;
  if(eta < 4.444) return 0.8366;
  if(eta < 4.722) return 0.6497;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_50(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
Forward jet pt cut of 50 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0233;
  if(eta < 0.556) return 1.0288;
  if(eta < 0.833) return 1.0211;
  if(eta < 1.111) return 1.0265;
  if(eta < 1.389) return 1.0146;
  if(eta < 1.667) return 0.9701;
  if(eta < 1.944) return 1.0112;
  if(eta < 2.222) return 1.0077;
  if(eta < 2.500) return 0.9747;
  if(eta < 2.778) return 0.9808;
  if(eta < 3.056) return 0.9525;
  if(eta < 3.333) return 0.9095;
  if(eta < 3.611) return 1.0222;
  if(eta < 3.889) return 0.9123;
  if(eta < 4.167) return 1.0626;
  if(eta < 4.444) return 0.8832;
  if(eta < 4.722) return 0.5845;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}