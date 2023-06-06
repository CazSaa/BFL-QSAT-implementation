import unittest

from z3 import Bools

from main import main

iw, h3, it, h2, pp, h1, h4, is_, h5, ab, mv, ut, vw = \
    map(lambda b: b.decl(), Bools("IW H3 IT H2 PP H1 H4 IS H5 AB MV UT VW"))


class MainTest(unittest.TestCase):
    maxDiff = None

    def test_main(self):
        self.assertListEqual(
            main('''
        toplevel IWoS;
        IWoS and CPR MoT SH;
        CPR or CP CR;
        CP and IW H3;
        CR and IT H2;
        MoT or CT DT AT CVT UT;
        CT or CIW CIO CIS;
        CIW and IW PP H1;
        CIO and IT MH1;
        MH1 and H1 H4;
        CIS and IS MH2;
        MH2 and H1 H5;
        DT and IW PP;
        AT and IW AB;
        CVT and IW MV H1;
        SH and VW H1;
        ---
        \\forall(IS => MoT);

        \\forall(MoT => (H1 || H2 || H3 || H4 || H5));
        
        \\forall H4 => IWoS; // parentheses not mandatory
        
        \\forall(\\vot[>= 2](H1,H2,H3,H4,H5) => IWoS);
        
        [[\\mcs(IWoS) && H4]];
        
        \\exists \\mps(IWoS)[H1: 0, H2: 0,H3: 0,H4: 0,H5: 0, IW: 1, IT: 1, 
        PP: 1, IS: 1, AB: 1, MV: 1, UT: 1, VW: 1]; // hmmmm
        
        [[\\mps(IWoS)]];
        
        //\\idp(CIO,CIS);
        
        //\\SUP(PP);
        
        // below by me
        UT, IW, H3 |= CPR && MoT;
        UT, IW, H3 |= CPR && MoT && SH;
        
        \\forall (CPR == CIW);
        
        \\forall (CPR != CIW);
        
        \\forall (!IS => !CIS);
        
        UT |= SH[VW: 1, H1: 1];
        
        UT |= !MoT[UT:0];
        '''),
            [
                False,  # \\forall(IS => MoT);
                False,  # \\forall(MoT => (H1 || H2 || H3 || H4 || H5));
                False,  # \\forall H4 => IWoS; // parentheses not mandatory
                False,  # \\forall(\\vot[>= 2](H1,H2,H3,H4,H5) => IWoS);
                {frozenset({iw, h3, it, h1, h4, vw}),
                 frozenset({it, h2, h1, h4, vw})},  # [[\\mcs(IWoS) && H4]];
                False,  # \\exists \\mps(IWoS)[H1: 0, H2: 0,H3: 0,H4: 0,H5: 0]
                {frozenset({iw, it}), frozenset({iw, h2}),
                 frozenset({iw, h4, is_, ut}), frozenset({iw, h4, h5, ut}),
                 frozenset({h3, it}), frozenset({h3, h2}),
                 frozenset({it, pp, is_, ab, mv, ut}),
                 frozenset({it, pp, h5, ab, mv, ut}),
                 frozenset({pp, h4, is_, ab, mv, ut}),
                 frozenset({pp, h4, h5, ab, mv, ut}), frozenset({h1}),
                 frozenset({vw})},  # [[\\mps(IWoS)]];
                # False,  # \\idp(CIO,CIS)
                # False,  # \\SUP(PP)
                True,  # UT, IW, H3 |= CPR && MoT
                False,  # UT, IW, H3 |= CPR && MoT && SH
                False,  # \\forall (CPR == CIW)
                False,  # \\forall (CPR != CIW)
                True,  # \\forall (!IS => !CIS)
                True,  # UT |= SH[VW: 1, H1: 1];
                True,  # UT |= !MoT[UT:0];
            ]
        )
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
