TEST_CASES = [
    {
        "ciphertext": f"""
        Dlc aygmo zbsux jmh nswtq yzcb xfo pyjc byk urmjo xfo wsx wcdw
        qvsuvc zolgxh rri bswrkrr wssxxysrq.
        """,
        "real_key": "KEY",
        "language": "en",
        "plaintext":f"""
        The quick brown fox jumps over the lazy dog while the sun sets
        slowly behind the distant mountains.
        """,
    },
    {
        "ciphertext": f"""
        Llk klwuo hlfkf jur aiety imsj xny corc jix kzmry kvw wah jslw
        yffkdc hyywfh zbv rawzueh esahkoary.
        """,
        "real_key": "SEGURO",
        "language": "en",
        "plaintext":f"""
        The quick brown fox jumps over the lazy dog while the sun sets
        slowly behind the distant mountains.
        """,
    },
    {
        "ciphertext": f"""
        Lgc tjgqz vduzn rgw hxbng dpqx whq dzxb smu lburh ttw rsq hchh
        mxuzlk tdflcb hwy povtmfs krjlhpczy, saufsgqv rvt mwe ln ezzbhh
        mt dlmtje mfc nxgnzt ue zke naqbv gchjlz zr ttwhp qtqhh zax whq
        fheki, qwcautj ttwhp ixloa matjs nwemut rvt xmxnnqkr qhirztm ut.
        """,
        "real_key": "SZYDPYOPUMGDAM",
        "language": "en",
        "plaintext":f"""
        The quick brown fox jumps over the lazy dog while the sun sets
        slowly behind the distant mountains, painting the sky in shades
        of orange and purple as the birds return to their nests for the
        night, singing their final songs before the darkness settles in.
        """,
    },
    {
        "ciphertext": f"""
        Q yaos tvep e tvuke fv rzm fl Rjqc lnlycutj s ihtj hqymde
        vyaiuwplvqgutz wqirz s vhpzxg cemqgshj, wquhvrfv cjq rlisiu
        kopvckon uwl nvhccah io bm geiv cmmuaagmpv pmóbkto à apqyenxc
        vnyi cz árqstls xvgzcdeo hloeu l vzvfls nsd v cép ebbl xpcyo.
        """,
        "real_key": "CHAVE",
        "language": "ptbr",
        "plaintext":f"""
        O rato roeu a roupa do rei de Roma enquanto o gato dormia
        tranquilamente sobre o tapete vermelho, sonhando com peixes
        dourados que nadavam em um lago cristalino próximo à floresta
        onde as árvores cresciam altas e verdes sob o céu azul claro        
        """,
    },
    {
        "ciphertext": f"""
        A znao tvep e dwhwa fv rzm pm Evmc lnlymvgv o ihtj hazzpa
        vyaiugqyhmgutz wajel o vhpzxq drymgshj, wavuhnfv cjq bmveeu
        kopvmlbz qwl nvhmdnt eo bm gesw pyiuaagmzw cyóxkto à apazrztc
        vnyi ma áecotls xvqappao hloee m ilrfls nsn w péb abbl xpmzb.
        """,
        "real_key": "MINHACHAVE",
        "language": "ptbr",
        "plaintext":f"""
        O rato roeu a roupa do rei de Roma enquanto o gato dormia
        tranquilamente sobre o tapete vermelho, sonhando com peixes
        dourados que nadavam em um lago cristalino próximo à floresta
        onde as árvores cresciam altas e verdes sob o céu azul claro        
        """,
    },
    {
        "ciphertext": f"""
        OAME. Ka wwcft ha ddrgcufx
        Tdewqotq hwy fqahg orsmud mh ulcc snye?
        Hy'w gemy xzzr K aht?
        FSAYZZ. Tr, by sbsv kmtl;
        'Wxq pjn fgk vwapba ge y yqit wcj mqd,
        Zkt nmzi smb pww ifs ibumm.
        ETRFEEE. Amvp, edrv; d, jmqjrc!
        HQYIFZ. M, og jdmr aidc, cktn U jek kgmm wwgg buuc,
        O iduzq cgt uqvggmih eumj. Wwedr mk xmwz uxlu,
        Php, kurz yah, lwqc'u grjp ztnfdx. Wwie vx kzwu:
        'Ektl tgiy le ixnsrv qns eiq vch ibur xlcg,
        Mah sqc dg pt uwib ogoos,' efp. Xzhq ka gdls.
        Lcxk erj bq zmfd lqe bds ogy pnaeay ibr?
        TDPVZDB. Gt hbq, le oxesr, gsm kcsh bc ycii snlh cxrejkw,
        K'to amjt bqq jhprxl, indp, gdhg bsplxx.
        NHAEZN. Mx hr cxstyf cif ordxn, mah hqmxm xcrfjy,
        Pdggay pvzgqag awtn ptnidkq be mah qns!
        Q ub scog gasnhg, da V wwd wqc oxtwca?
        XZLHJ. Muai wxcu aptjz dhuntv; X stnpd vcgx dcmb.
        Viac Zrb Ddhq, ddlf uh p focxwdxfwed. Fs, A
        sfcvn ifst. Qmhz rc mq used, G'nt ppis hjaqz zxtt glwd;
        jgb www qjlfrohh axbrw, sfgg dgc grodue rcee.
        XMFF. Jgb xh dfdg bnoqi ta csamr vplh qhdlk jtrl,
        Ta zecd rjm hkcb ilgsn lc pxrektpg nodu.
        Wu ntna eteeg cws y hzhhf icwdnvstd rysodp,
        Eprdqs ibat zkn hgffsmb, cvg X'jz euk snb soirv;
        Xnp K kdc eitme sndi bk glq gmpmvi yws
        Ntna ntpf'fx s vghm ktpgtfr, snbhexs e ezgf.-
        Wi ifoi uzc goa ttr tjnetmvh, kcgy mmj otse,
        Eiknjxmgaw adlq kklhudr wzzjn maepshm.
        Mkr btt erier ugto; plr xz us kqs sa ziws,
        Rjm exrhtl bzyw, bodr awkaquh xq hwy evkhi.
        """,
        "real_key": "ESZYCIDPYOPUMZGDPAMN",
        "language": "en",
        "plaintext": """
        KING. Is there no exorcist
        Beguiles the truer office of mine eyes?
        Is't real that I see?
        HELENA. No, my good lord;
        'Tis but the shadow of a wife you see,
        The name and not the thing.
        BERTRAM. Both, both; o, pardon!
        HELENA. O, my good lord, when I was like this maid,
        I found you wondrous kind. There is your ring,
        And, look you, here's your letter. This it says:
        'When from my finger you can get this ring,
        And are by me with child,' etc. This is done.
        Will you be mine now you are doubly won?
        BERTRAM. If she, my liege, can make me know this clearly,
        I'll love her dearly, ever, ever dearly.
        HELENA. If it appear not plain, and prove untrue,
        Deadly divorce step between me and you!
        O my dear mother, do I see you living?
        LAFEU. Mine eyes smell onions; I shall weep anon.
        Good Tom Drum, lend me a handkercher. So, I
        thank thee. Wait on me home, I'll make sport with thee;
        let thy curtsies alone, they are scurvy ones.
        KING. Let us from point to point this story know,
        To make the even truth in pleasure flow.
        If thou beest yet a fresh uncropped flower,
        Choose thou thy husband, and I'll pay thy dower;
        For I can guess that by thy honest aid
        Thou kept'st a wife herself, thyself a maid.-
        Of that and all the progress, more and less,
        Resolvedly more leisure shall express.
        All yet seems well; and if it end so meet,
        The bitter past, more welcome is the sweet.
        """
    },
    {
        "ciphertext": f"""
        Hs mmuad kgrp, yy lkld dm wsjmyfi,
        Drfsx-gq mapp sqyzs scpmegmgp,
        3 Nqmjr eedqmvn y xmusyrtcdz kvirmqe.

        Vhxgz tjyz tlm é buxha fãb twmmui,
        Gtqhp vdzbd tsbrwktpc i dhnsgcpzjh,
        6 Fuq n qwlópki d gcztgnqg lcdm pyacmui.

        Qp kcgnq gá vrjca zear bg iftppxxmck;
        Pps bnvs n zgu qppfpl xá cksprmqs
        9 Vd mwbupq qdoezy tje hv, haqck dhgbosy.

        Ontwpr zãb tgrqq krbm hxhtz kqirmqs;
        Lzlvw r hmbd ie rkqiipbw ed rqudgy,
        12 Ejuzcu kti a ose byoqqwm oquzcuqpda.

        Qihngu yxt y ibu onrlca yr gwqaczd,
        Dlrt cm n bdae qfgmqm vmubgbphpn,
        15 Wxt pmisj sãm rzrusbsi yd idjsmee.

        Sn ynbr djvtc, q iá, jh aul oefgyplr,
        Kg-zwy qrzdg às qftskbca r ejocyfz,
        18 Wxt, cqexg, dk vwgp nognq ugl vuunrvn.

        Cpbãr d yghiyaxr jm fnrln qg itjgsiu,
        Ctk gd pqvxg mm nijd nsgxgqgyp,
        21 Nmdywky pwlic oiluaaopdm, vritggbd.

        T acbi ctkp d azéymln cuoriyjp
        Maaxh ps aahsr, há uiokm, wcxm lkggoeb
        24 Sdgy q udg nsgcsnyr tm chi dtrcdd,

        D ksj âhulu dhsuz, umd rtmpt ybhcaru,
        Ydlhry-kd y tmpxpog pqmilso a rwhzçm
        27 Sch wmatg hhbr yaynmk oyuarj bwiien.

        Zhcda wá vwomwadsm c ridou opseb,
        Wwfsk xhay rtmqqzd uaxqe suypbh;
        30 Bywh vmhdr hezqs g oé dkzpt lc eueru.
        """,
        "language": "ptbr",
        "real_key": "ESZYCIDPYOPUMZGDPAMN",
        "plaintext": f"""
        Da nossa vida, em meio da jornada,
        Achei-me numa selva tenebrosa,
        3 Tendo perdido a verdadeira estrada.

        Dizer qual era é cousa tão penosa,
        Desta brava espessura a asperidade,
        6 Que a memória a relembra inda cuidosa.

        Na morte há pouco mais de acerbidade;
        Mas para o bem narrar lá deparado
        9 De outras cousas que vi, direi verdade.

        Contar não posso como tinha entrado;
        Tanto o sono os sentidos me tomara,
        12 Quando hei o bom caminho abandonado.

        Depois que a uma colina me cercara,
        Onde ia o vale escuro terminando,
        15 Que pavor tão profundo me causara.

        Ao alto olhei, e já, de luz banhando,
        Vi-lhe estar às espaldas o planeta,
        18 Que, certo, em toda parte vai guiando.

        Então o assombro um tanto se aquieta,
        Que do peito no lago perdurava,
        21 Naquela noite atribulada, inquieta.

        E como quem o anélito esgotava
        Sobre as ondas, já salvo, inda medroso
        24 Olha o mar perigoso em que lutava,

        O meu ânimo assim, que treme ansioso,
        Volveu-se a remirar vencido o espaço
        27 Que homem vivo jamais passou ditoso.

        Tendo já repousado o corpo lasso,
        Segui pela deserta falda avante;
        30 Mais baixo sendo o pé firme no passo.
        """,
    },
]