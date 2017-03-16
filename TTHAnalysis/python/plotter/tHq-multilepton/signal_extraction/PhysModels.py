from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
from HiggsAnalysis.CombinedLimit.LHCHCGModels import LHCHCGBaseModel
import ROOT

class KappaVKappaT(LHCHCGBaseModel):
    def __init__(self,resolved=True,BRU=True,addInvisible=False):
        LHCHCGBaseModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.doBRU = BRU
        self.resolved = resolved
        self.addInvisible = addInvisible
    def setPhysicsOptions(self,physOptions):
        self.setPhysicsOptionsBase(physOptions)
        for po in physOptions:
            if po.startswith("BRU="):
                self.doBRU = (po.replace("BRU=","") in [ "yes", "1", "Yes", "True", "true" ])
        print "BR uncertainties in partial widths: %s " % self.doBRU
    def doParametersOfInterest(self):
        """Create POI out of signal strength and MH"""
        self.modelBuilder.doVar("r[1,0.0,10.0]") 
        self.modelBuilder.doVar("kappa_V[1,0.0,2.0]") 
        self.modelBuilder.doVar("kappa_t[1,-4.0,4.0]")
        self.modelBuilder.doVar("kappa_tau[1,0.0,3.0]")
        self.modelBuilder.doVar("kappa_mu[1,0.0,5.0]") 
        self.modelBuilder.factory_("expr::kappa_mu_expr(\"@0*@1+(1-@0)*@2\", CMS_use_kmu[0], kappa_mu, kappa_tau)")
        self.modelBuilder.doVar("kappa_b[1,0.0,3.0]")
        self.modelBuilder.doVar("kappa_c[1,0.0,3.0]") # treat hcc independently from kappa_t
        if not self.resolved:
            self.modelBuilder.doVar("kappa_g[1,0.0,2.0]")
            self.modelBuilder.doVar("kappa_gam[1,0.0,2.5]")
        self.modelBuilder.doVar("BRinv[0,0,1]")
        if not self.addInvisible: self.modelBuilder.out.var("BRinv").setConstant(True)
        pois = 'kappa_V,kappa_tau,kappa_t,kappa_b,kappa_c'
        if not self.resolved:
            pois += ',kappa_g,kappa_gam'
        if self.addInvisible: pois+=",BRinv"
        self.doMH()
        self.modelBuilder.doSet("POI",pois)
        self.SMH = SMHiggsBuilder(self.modelBuilder)
        self.setup()

    def setup(self):
        self.dobbH()
        # SM BR
        for d in SM_HIGG_DECAYS + [ "hss" ]: 
            self.SMH.makeBR(d)
        # BR uncertainties
        if self.doBRU:
            self.SMH.makePartialWidthUncertainties()
        else:
            for d in SM_HIGG_DECAYS: 
                self.modelBuilder.factory_('HiggsDecayWidth_UncertaintyScaling_%s[1.0]' % d)
        # get VBF, tHq, tHW, ggZH cross section
        self.SMH.makeScaling('qqH', CW='kappa_V', CZ='kappa_V')
        self.SMH.makeScaling("tHq", CW='kappa_V', Ctop="kappa_t")
        self.SMH.makeScaling("tHW", CW='kappa_V', Ctop="kappa_t")
        self.SMH.makeScaling("ggZH", CZ='kappa_V', Ctop="kappa_t",Cb="kappa_b")
        # resolve loops
        if self.resolved:
            self.SMH.makeScaling('ggH', Cb='kappa_b', Ctop='kappa_t', Cc="kappa_t")
            self.SMH.makeScaling('hgluglu', Cb='kappa_b', Ctop='kappa_t')
            self.SMH.makeScaling('hgg', Cb='kappa_b', Ctop='kappa_t', CW='kappa_V', Ctau='kappa_tau')
            self.SMH.makeScaling('hzg', Cb='kappa_b', Ctop='kappa_t', CW='kappa_V', Ctau='kappa_tau')
        else:
            self.modelBuilder.factory_('expr::Scaling_hgluglu("@0*@0", kappa_g)')
            self.modelBuilder.factory_('expr::Scaling_hgg("@0*@0", kappa_gam)')
            self.modelBuilder.factory_('expr::Scaling_hzg("@0*@0", kappa_gam)')
            self.modelBuilder.factory_('expr::Scaling_ggH_7TeV("@0*@0", kappa_g)')
            self.modelBuilder.factory_('expr::Scaling_ggH_8TeV("@0*@0", kappa_g)')
            self.modelBuilder.factory_('expr::Scaling_ggH_13TeV("@0*@0", kappa_g)')
            self.modelBuilder.factory_('expr::Scaling_ggH_14TeV("@0*@0", kappa_g)')

        ## partial witdhs, normalized to the SM one
        self.modelBuilder.factory_('expr::c7_Gscal_Z("@0*@0*@1*@2", kappa_V, SM_BR_hzz, HiggsDecayWidth_UncertaintyScaling_hzz)')
        self.modelBuilder.factory_('expr::c7_Gscal_W("@0*@0*@1*@2", kappa_V, SM_BR_hww, HiggsDecayWidth_UncertaintyScaling_hww)')
        self.modelBuilder.factory_('expr::c7_Gscal_tau("@0*@0*@1*@4+@2*@2*@3*@5", kappa_tau, SM_BR_htt, kappa_mu_expr, SM_BR_hmm, HiggsDecayWidth_UncertaintyScaling_htt, HiggsDecayWidth_UncertaintyScaling_hmm)')
        self.modelBuilder.factory_('expr::c7_Gscal_top("@0*@0 * @1*@2", kappa_c, SM_BR_hcc, HiggsDecayWidth_UncertaintyScaling_hcc)')
        self.modelBuilder.factory_('expr::c7_Gscal_bottom("@0*@0 * (@1*@3+@2)", kappa_b, SM_BR_hbb, SM_BR_hss, HiggsDecayWidth_UncertaintyScaling_hbb)')
        self.modelBuilder.factory_('expr::c7_Gscal_gluon("  @0  * @1 * @2", Scaling_hgluglu, SM_BR_hgluglu, HiggsDecayWidth_UncertaintyScaling_hgluglu)')
        self.modelBuilder.factory_('expr::c7_Gscal_gamma("@0*@1*@4 + @2*@3*@5",  Scaling_hgg, SM_BR_hgg, Scaling_hzg, SM_BR_hzg, HiggsDecayWidth_UncertaintyScaling_hgg, HiggsDecayWidth_UncertaintyScaling_hzg)')
        # fix to have all BRs add up to unity
        self.modelBuilder.factory_("sum::c7_SMBRs(%s)" %  (",".join("SM_BR_"+X for X in "hzz hww htt hmm hcc hbb hss hgluglu hgg hzg".split())))
        self.modelBuilder.out.function("c7_SMBRs").Print("")        

        ## total witdh, normalized to the SM one
        self.modelBuilder.factory_('expr::c7_Gscal_tot("(@1+@2+@3+@4+@5+@6+@7)/@8/(1-@0)", BRinv, c7_Gscal_Z, c7_Gscal_W, c7_Gscal_tau, c7_Gscal_top, c7_Gscal_bottom, c7_Gscal_gluon, c7_Gscal_gamma, c7_SMBRs)')

        ## BRs, normalized to the SM ones: they scale as (partial/partial_SM) / (total/total_SM) 
        self.modelBuilder.factory_('expr::c7_BRscal_hww("@0*@0*@2/@1", kappa_V, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hww)')
        self.modelBuilder.factory_('expr::c7_BRscal_hzz("@0*@0*@2/@1", kappa_V, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hzz)')
        self.modelBuilder.factory_('expr::c7_BRscal_htt("@0*@0*@2/@1", kappa_tau, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_htt)')
        self.modelBuilder.factory_('expr::c7_BRscal_hmm("@0*@0*@2/@1", kappa_mu_expr, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hmm)')
        self.modelBuilder.factory_('expr::c7_BRscal_hbb("@0*@0*@2/@1", kappa_b, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hbb)')
        self.modelBuilder.factory_('expr::c7_BRscal_hcc("@0*@0*@2/@1", kappa_c, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hcc)')
        self.modelBuilder.factory_('expr::c7_BRscal_hgg("@0*@2/@1", Scaling_hgg, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hgg)')
        self.modelBuilder.factory_('expr::c7_BRscal_hzg("@0*@2/@1", Scaling_hzg, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hzg)')
        self.modelBuilder.factory_('expr::c7_BRscal_hgluglu("@0*@2/@1", Scaling_hgluglu, c7_Gscal_tot, HiggsDecayWidth_UncertaintyScaling_hgluglu)')

        self.modelBuilder.factory_('expr::c7_BRscal_hinv("@0", BRinv)')

    def getYieldScale(self,bin,process):
        """Scale ttH as tHq and tHW, even if it's not listed as signal in the datacards"""
        if not self.DC.isSignal[process]: return 1 ## FIXME
        (processSource, foundDecay, foundEnergy) = getHiggsProdDecMode(bin,process,self.options)
        return self.getHiggsSignalYieldScale(processSource, foundDecay, foundEnergy)

    def getHiggsSignalYieldScale(self,production,decay,energy):
        name = "c7_XSBRscal_%s_%s_%s" % (production,decay,energy)
        if self.modelBuilder.out.function(name) == None:
            if production in [ "ggH", "qqH", "ggZH", "tHq", "tHW"]: 
                XSscal = ("@0", "Scaling_%s_%s" % (production,energy) )
            elif production == "WH":  XSscal = ("@0*@0", "kappa_V")
            elif production == "ZH":  XSscal = ("@0*@0", "kappa_V")
            elif production == "ttH": XSscal = ("@0*@0", "kappa_t")
            elif production == "bbH": XSscal = ("@0*@0", "kappa_b")
            else: raise RuntimeError, "Production %s not supported" % production
            BRscal = decay
            if not self.modelBuilder.out.function("c7_BRscal_"+BRscal):
                raise RuntimeError, "Decay mode %s not supported" % decay
            if decay == "hss": BRscal = "hbb"
            if production in ['tHq', 'tHW', 'ttH']:
                self.modelBuilder.factory_('expr::%s("%s*@1*@2", %s, c7_BRscal_%s, r)' % (name, XSscal[0], XSscal[1], BRscal))
            elif production == "ggH" and (decay in self.add_bbH) and energy in ["7TeV","8TeV","13TeV","14TeV"]:
                b2g = "CMS_R_bbH_ggH_%s_%s[%g]" % (decay, energy, 0.01) 
                b2gs = "CMS_bbH_scaler_%s" % energy
                self.modelBuilder.factory_('expr::%s("(%s + @1*@1*@2*@3)*@4", %s, kappa_b, %s, %s, c7_BRscal_%s)' % (name, XSscal[0], XSscal[1], b2g, b2gs, BRscal))
            else:
                self.modelBuilder.factory_('expr::%s("%s*@1", %s, c7_BRscal_%s)' % (name, XSscal[0], XSscal[1], BRscal))
            print '[LHC-HCG Kappas]', name, production, decay, energy,": ",
            self.modelBuilder.out.function(name).Print("")
        return name

class KappaVKappaFWithr(LHCHCGBaseModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self,BRU=True,floatbrinv=False):
        LHCHCGBaseModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.doBRU = BRU
    self.floatbrinv = floatbrinv
    def setPhysicsOptions(self,physOptions):
        self.setPhysicsOptionsBase(physOptions)
        for po in physOptions:
            if po.startswith("BRU="):
                self.doBRU = (po.replace("BRU=","") in [ "yes", "1", "Yes", "True", "true" ])
        print "BR uncertainties in partial widths: %s " % self.doBRU
    def doParametersOfInterest(self):
        """Create POI out of signal strength and MH"""
        self.modelBuilder.doVar("r[1,0.0,10.0]")
        self.modelBuilder.doVar("kappa_V[1,0.0,2.0]")
        self.modelBuilder.doVar("kappa_F[1,-4.0,4.0]")
        self.modelBuilder.doVar("BRinv[0,0,1]")
    self.modelBuilder.out.var("BRinv").setConstant()
        for d in ["WW","ZZ","gamgam","bb","tautau","mumu","inv"]:
            self.modelBuilder.doVar("kappa_V_%s[1,0.0,2.0]"%d)
            self.modelBuilder.doVar("kappa_F_%s[1,-2.0,2.0]"%d)
            self.modelBuilder.out.var("kappa_V_"+d).setConstant()
            self.modelBuilder.out.var("kappa_F_"+d).setConstant()
        pois = 'kappa_V,kappa_F'
    if self.floatbrinv : 
        self.modelBuilder.out.var("BRinv").setConstant(False)
        pois+=',BRinv'
        self.doMH()
        self.modelBuilder.doSet("POI",pois)
        self.SMH = SMHiggsBuilder(self.modelBuilder)
        self.setup()

    def setup(self):
        self.dobbH()
        # SM BR
        for d in SM_HIGG_DECAYS + [ "hss" ]:
            self.SMH.makeBR(d)
        # BR uncertainties
        if self.doBRU:
            self.SMH.makePartialWidthUncertainties()
        else:
            for d in SM_HIGG_DECAYS:
                self.modelBuilder.factory_('HiggsDecayWidth_UncertaintyScaling_%s[1.0]' % d)

        # fix to have all BRs add up to unity
        self.modelBuilder.factory_("sum::c7_SMBRs(%s)" %  (",".join("SM_BR_"+X for X in "hzz hww htt hmm hcc hbb hss hgluglu hgg hzg".split())))
        self.modelBuilder.out.function("c7_SMBRs").Print("")

        for ds in ["WW","ZZ","gamgam","bb","tautau","mumu","inv"]:
            self.modelBuilder.factory_('expr::kVkV_%s("@0*@1", kappa_V,kappa_V_%s)' % (ds,ds))
            self.modelBuilder.factory_('expr::kFkF_%s("@0*@1", kappa_F,kappa_F_%s)' % (ds,ds))

            # get tHq, tHW, ggZH cross section
            self.SMH.makeScaling("tHq_"+ds, CW='kVkV_'+ds, Ctop="kFkF_"+ds)
            self.SMH.makeScaling("tHW_"+ds, CW='kVkV_'+ds, Ctop="kFkF_"+ds)
            self.SMH.makeScaling("ggZH_"+ds, CZ='kVkV_'+ds, Ctop="kFkF_"+ds, Cb="kFkF_"+ds)
            # resolve hgg, hzg loops
            self.SMH.makeScaling("hgg_"+ds, Cb='kFkF_'+ds, Ctop='kFkF_'+ds, CW='kVkV_'+ds, Ctau='kFkF_'+ds)
            self.SMH.makeScaling("hzg_"+ds, Cb='kFkF_'+ds, Ctop='kFkF_'+ds, CW='kVkV_'+ds, Ctau='kFkF_'+ds)
            ## partial witdhs, normalized to the SM one
            self.modelBuilder.factory_('expr::c7_Gscal_Z_%s("@0*@0*@1*@2", kVkV_%s, SM_BR_hzz, HiggsDecayWidth_UncertaintyScaling_hzz)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_W_%s("@0*@0*@1*@2", kVkV_%s, SM_BR_hww, HiggsDecayWidth_UncertaintyScaling_hww)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_tau_%s("@0*@0*@1*@3+@0*@0*@2*@4", kFkF_%s, SM_BR_htt, SM_BR_hmm, HiggsDecayWidth_UncertaintyScaling_htt, HiggsDecayWidth_UncertaintyScaling_hmm)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_top_%s("@0*@0 * @1*@2", kFkF_%s, SM_BR_hcc, HiggsDecayWidth_UncertaintyScaling_hcc)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_bottom_%s("@0*@0 * (@1*@3+@2)", kFkF_%s, SM_BR_hbb, SM_BR_hss, HiggsDecayWidth_UncertaintyScaling_hbb)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_gluon_%s("  @0*@0*@1*@2", kFkF_%s, SM_BR_hgluglu, HiggsDecayWidth_UncertaintyScaling_hgluglu)' % (ds,ds))
            self.modelBuilder.factory_('expr::c7_Gscal_gamma_%s("@0*@1*@4 + @2*@3*@5",  Scaling_hgg_%s, SM_BR_hgg, Scaling_hzg_%s, SM_BR_hzg, HiggsDecayWidth_UncertaintyScaling_hgg, HiggsDecayWidth_UncertaintyScaling_hzg)' % (ds,ds,ds))

            ## total witdh, normalized to the SM one
            self.modelBuilder.factory_('expr::c7_Gscal_tot_%s("(@0+@1+@2+@3+@4+@5+@6)/@7/(1-@8)", c7_Gscal_Z_%s, c7_Gscal_W_%s, c7_Gscal_tau_%s, c7_Gscal_top_%s, c7_Gscal_bottom_%s, c7_Gscal_gluon_%s, c7_Gscal_gamma_%s, c7_SMBRs, BRinv)' % (ds,ds,ds,ds,ds,ds,ds,ds))

        ## BRs, normalized to the SM ones: they scale as (partial/partial_SM) / (total/total_SM) 
        for d in ["hww","hzz"]:
            self.modelBuilder.factory_('expr::c7_BRscal_%s("@0*@0*@2/@1", kVkV_%s, c7_Gscal_tot_%s, HiggsDecayWidth_UncertaintyScaling_%s)' % (d,CMS_to_LHCHCG_DecSimple[d], CMS_to_LHCHCG_DecSimple[d], d))
        for d in ["htt","hmm","hbb","hcc","hgluglu"]:
            self.modelBuilder.factory_('expr::c7_BRscal_%s("@0*@0*@2/@1", kFkF_%s, c7_Gscal_tot_%s, HiggsDecayWidth_UncertaintyScaling_%s)' % (d,CMS_to_LHCHCG_DecSimple[d], CMS_to_LHCHCG_DecSimple[d], d))
        for d in ["hgg","hzg"]:
            self.modelBuilder.factory_('expr::c7_BRscal_%s("@0*@2/@1", Scaling_%s_%s, c7_Gscal_tot_%s, HiggsDecayWidth_UncertaintyScaling_%s)' % (d,d,CMS_to_LHCHCG_DecSimple[d], CMS_to_LHCHCG_DecSimple[d], d))

    # H->invisible scaling 
    self.modelBuilder.factory_('expr::c7_BRscal_hinv("@0", BRinv)')
 
    def getHiggsSignalYieldScale(self,production,decay,energy):
        name = "c7_XSBRscal_%s_%s_%s" % (production,decay,energy)
        if self.modelBuilder.out.function(name) == None:
            if production in [ "ggZH", "tHq", "tHW"]:
                XSscal = ("@0", "Scaling_%s_%s_%s" % (production,CMS_to_LHCHCG_DecSimple[decay],energy) )
            elif production in ["ggH", "ttH", "bbH"]:  XSscal = ("@0*@0", "kFkF_"+CMS_to_LHCHCG_DecSimple[decay])
            elif production in ["qqH", "WH", "ZH"]:  XSscal = ("@0*@0", "kVkV_"+CMS_to_LHCHCG_DecSimple[decay])
            else: raise RuntimeError, "Production %s not supported" % production
            BRscal = decay
            if decay == "hss": BRscal = "hbb"
            if not self.modelBuilder.out.function("c7_BRscal_"+BRscal):
                raise RuntimeError, "Decay mode %s not supported" % decay
            if production == "ggH" and (decay in self.add_bbH) and energy in ["7TeV","8TeV","13TeV","14TeV"]:
                b2g = "CMS_R_bbH_ggH_%s_%s[%g]" % (decay, energy, 0.01)
                b2gs = "CMS_bbH_scaler_%s" % energy
                self.modelBuilder.factory_('expr::%s("(%s + @1*@1*@2*@3)*@4", %s, kFkF_%s, %s, %s, c7_BRscal_%s)' % (name, XSscal[0], XSscal[1], CMS_to_LHCHCG_DecSimple[decay], b2g, b2gs, BRscal))
            else:
                self.modelBuilder.factory_('expr::%s("%s*@1*@2", %s, c7_BRscal_%s,r)' % (name, XSscal[0], XSscal[1], BRscal))
            print '[LHC-HCG Kappas]', name, production, decay, energy,": ",
            self.modelBuilder.out.function(name).Print("")
        return name

class LambdasReducedWithr(LHCHCGBaseModel):
    """
    Copied from https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/74x-root6/python/LHCHCGModels.py#L626-L788
    
    Changed lambda_FV range from 0,2.0 to -10.0,10.0
    Added signal strength parameter r back in

    """
    def __init__(self,BRU=True,model="",addInvisible=False):
        LHCHCGBaseModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.doBRU = BRU
        self.model = model
        self.addInvisible = addInvisible
    def setPhysicsOptions(self,physOptions):
        self.setPhysicsOptionsBase(physOptions)
        for po in physOptions:
            if po.startswith("BRU="):
                self.doBRU = (po.replace("BRU=","") in [ "yes", "1", "Yes", "True", "true" ])
        print "BR uncertainties in partial widths: %s " % self.doBRU
    def doParametersOfInterest(self):
        """Create POI out of signal strength and MH"""
        self.doMH()
        self.modelBuilder.doVar("lambda_FV[1,-10.0,10.0]")
        self.modelBuilder.doVar("kappa_VV[1,0.0,2.0]")
        self.modelBuilder.doVar("lambda_du[1,0.0,2.0]")
        self.modelBuilder.doVar("lambda_Vu[1,0.0,2.0]")
        self.modelBuilder.doVar("kappa_uu[1,0.0,2.0]")
        self.modelBuilder.doVar("lambda_lq[1,0.0,2.0]")
        self.modelBuilder.doVar("lambda_Vq[1,0.0,2.0]")
        self.modelBuilder.doVar("kappa_qq[1,0.0,2.0]")
        self.modelBuilder.doVar("r[1,0.0,10.0]")

        self.modelBuilder.doVar("BRinv[0,0,1]")
        if not self.addInvisible: self.modelBuilder.out.var("BRinv").setConstant(True)

        POIset = 'lambda_FV,kappa_VV,lambda_du,lambda_Vu,kappa_uu,lambda_lq,lambda_Vq,kappa_qq'
        if self.model=="ldu":
          self.modelBuilder.out.var("lambda_du").setConstant(False)
          self.modelBuilder.out.var("kappa_uu").setConstant(False)
          self.modelBuilder.out.var("lambda_Vu").setConstant(False)

          self.modelBuilder.out.var("lambda_FV").setConstant(True)
          self.modelBuilder.out.var("kappa_VV").setConstant(True)
          self.modelBuilder.out.var("lambda_lq").setConstant(True)
          self.modelBuilder.out.var("lambda_Vq").setConstant(True)
          self.modelBuilder.out.var("kappa_qq").setConstant(True)

          POIset = 'lambda_du,lambda_Vu,kappa_uu'

        elif self.model=="llq": 
        
          self.modelBuilder.out.var("lambda_lq").setConstant(False)
          self.modelBuilder.out.var("lambda_Vq").setConstant(False)
          self.modelBuilder.out.var("kappa_qq").setConstant(False)

          self.modelBuilder.out.var("lambda_du").setConstant(True)
          self.modelBuilder.out.var("kappa_uu").setConstant(True)
          self.modelBuilder.out.var("lambda_Vu").setConstant(True)
          self.modelBuilder.out.var("lambda_FV").setConstant(True)
          self.modelBuilder.out.var("kappa_VV").setConstant(True)

          POIset = 'lambda_lq,lambda_Vq,kappa_qq'

        elif self.model=="lfv": 
        

          self.modelBuilder.out.var("lambda_FV").setConstant(False)
          self.modelBuilder.out.var("kappa_VV").setConstant(False)

          self.modelBuilder.out.var("lambda_lq").setConstant(True)
          self.modelBuilder.out.var("lambda_Vq").setConstant(True)
          self.modelBuilder.out.var("kappa_qq").setConstant(True)
          self.modelBuilder.out.var("lambda_du").setConstant(True)
          self.modelBuilder.out.var("kappa_uu").setConstant(True)
          self.modelBuilder.out.var("lambda_Vu").setConstant(True)

          POIset = 'lambda_FV,kappa_VV'

        self.modelBuilder.doSet("POI",POIset)
        if self.floatMass:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setRange(float(self.mHRange[0]),float(self.mHRange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
            else:
                self.modelBuilder.doVar("MH[%s,%s]" % (self.mHRange[0],self.mHRange[1]))
        else:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setVal(self.options.mass)
                self.modelBuilder.out.var("MH").setConstant(True)
            else:
                self.modelBuilder.doVar("MH[%g]" % self.options.mass)
        self.SMH = SMHiggsBuilder(self.modelBuilder)
        self.setup()

    def setup(self):
        self.dobbH()
        # BR uncertainties
        if self.doBRU:
            self.SMH.makePartialWidthUncertainties()

        self.modelBuilder.factory_("expr::C_b(\"@0*@1\",lambda_du,lambda_FV)");
        self.modelBuilder.factory_("expr::C_top(\"@0\",lambda_FV)");
        self.modelBuilder.factory_("expr::C_tau(\"@0*@1*@2\",lambda_lq,lambda_du, lambda_FV)");
        self.modelBuilder.factory_("expr::C_V(\"@0*@1\",lambda_Vq,lambda_Vu)");
        self.SMH.makeScaling('ggH', Cb='C_b', Ctop='C_top', Cc="C_top")
        self.SMH.makeScaling("tHq", CW='C_V', Ctop="C_top")
        self.SMH.makeScaling("tHW", CW='C_V', Ctop="C_top")
        self.SMH.makeScaling("ggZH", CZ='C_V', Ctop="C_top", Cb="C_b")
        self.SMH.makeScaling('hgg', Cb='C_b', Ctop='C_top', CW='C_V', Ctau='C_tau')
        self.SMH.makeScaling('hzg', Cb='C_b', Ctop='C_top', CW='C_V', Ctau='C_tau')
        self.SMH.makeScaling('hgluglu', Cb='C_b', Ctop='C_top')

        # H->invisible scaling 
        self.modelBuilder.factory_('expr::Scaling_hinv("@0", BRinv)')

        for E in "7TeV", "8TeV","13TeV","14TeV":
            for P in "ggH", "tHq", "tHW", "ggZH":
                self.modelBuilder.factory_("expr::PW_XSscal_%s_%s(\"@0*@1*@1*@2*@2*@3*@3\",Scaling_%s_%s,kappa_qq, kappa_uu, kappa_VV)"%(P,E,P,E))
            for P in "qqH", "WH", "ZH":
                self.modelBuilder.factory_("expr::PW_XSscal_%s_%s(\"@0*@0*@1*@1*@2*@2*@3*@3*@4*@4\", kappa_qq, lambda_Vq, kappa_uu, lambda_Vu, kappa_VV)" % (P,E))
            self.modelBuilder.factory_("expr::PW_XSscal_ttH_%s(\"@0*@0*@1*@1*@2*@2*@3*@3\",kappa_qq,kappa_uu,kappa_VV,lambda_FV)" % E)
            self.modelBuilder.factory_("expr::PW_XSscal_bbH_%s(\"@0*@0*@1*@1*@2*@2*@3*@3*@4*@4\",kappa_qq,kappa_uu,lambda_du,kappa_VV,lambda_FV)" % E)
        self.decayMap_ = {
            'hww' : 'C_V',
            'hzz' : 'C_V',
            'hgg' : 'Scaling_hgg',
            'hbb' : 'C_b',
            'htt' : 'C_tau',
            'hmm' : 'C_tau',
            'hcc' : 'C_top',     # charm scales as top
            'hgluglu' : 'Scaling_hgluglu',
            'hzg'     : 'Scaling_hzg',
            'hinv'     : 'Scaling_hinv',
            #'hss' : 'C_b', # strange scales as bottom # not used
        }

    def getHiggsSignalYieldScale(self,production,decay,energy):
        name = "c7_XSBRscal_%s_%s_%s" % (production,decay,energy)
        if self.modelBuilder.out.function(name):
            return name
        dscale = self.decayMap_[decay]
        if self.doBRU:
            name += "_noBRU"
        if production == "ggH":
            if decay in self.add_bbH:
                b2g = "CMS_R_bbH_ggH_%s_%s[%g]" % (decay, energy, 0.01)
                b2gs = "CMS_bbH_scaler_%s" % energy
                if decay in ["hgg","hgluglu","hzg"]:
                    self.modelBuilder.factory_("expr::%s(\"@0*@1*(1+@2*@3*@4)\",PW_XSscal_ggH_%s,%s,%s,%s,PW_XSscal_bbH_%s)" % (name, energy, dscale, b2g, b2gs, energy))
                else:
                    self.modelBuilder.factory_("expr::%s(\"@0*@1*@1*(1+@2*@3*@4)\",PW_XSscal_ggH_%s,%s,%s,%s,PW_XSscal_bbH_%s)" % (name, energy, dscale, b2g, b2gs, energy))
            else:
                if decay in ["hgg","hgluglu","hzg"]:
                    self.modelBuilder.factory_("expr::%s(\"@0*@1\",PW_XSscal_ggH_%s,%s)" % (name, energy, dscale))
                else:
                    self.modelBuilder.factory_("expr::%s(\"@0*@1*@1\",PW_XSscal_ggH_%s,%s)" % (name, energy, dscale))
        else:
            if decay in ["hgg","hgluglu","hzg"]:
                self.modelBuilder.factory_("expr::%s(\"@0*@1\",PW_XSscal_%s_%s,%s)" % (name, production, energy, dscale))
            else:
                # self.modelBuilder.factory_("expr::%s(\"@0*@1*@1\",PW_XSscal_%s_%s,%s)" % (name, production, energy, dscale))
                self.modelBuilder.factory_("expr::%s(\"@0*@1*@1*@2\",PW_XSscal_%s_%s,%s,r)" % (name, production, energy, dscale))
        if self.doBRU:
            name = name.replace("_noBRU","")
            if decay == "hzz":
                self.modelBuilder.factory_("prod::%s(%s_noBRU, HiggsDecayWidth_UncertaintyScaling_%s)" % (name, name, "hzz"))
            else:
                self.modelBuilder.factory_("expr::%s(\"@0*(@1/@2)\", %s_noBRU, HiggsDecayWidth_UncertaintyScaling_%s, HiggsDecayWidth_UncertaintyScaling_%s)" % (name, name, decay, "hzz"))
        print '[LHC-HCG Lambdas]', name, production, decay, energy,": ",
        self.modelBuilder.out.function(name).Print("")
        return name




L2 = LambdasReducedWithr()
K3 = KappaVKappaFWithr()

K4 = KappaVKappaT(resolved=True)
K5 = KappaVKappaT(resolved=False)
