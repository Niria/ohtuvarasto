import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)
        self.huono_varasto = Varasto(-1, -1)
        self.taysi_varasto = Varasto(10, 15)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_konstruktori_nollaa_tilavuuden(self):
        self.assertAlmostEqual(self.huono_varasto.tilavuus, 0.0)

    def test_konstruktori_nollaa_saldon(self):
        self.assertAlmostEqual(self.huono_varasto.saldo, 0.0)

    def test_konstruktori_asettaa_saldoksi_tilavuuden(self):
        self.assertAlmostEqual(self.taysi_varasto.saldo, 10)

    def test_lisays_ei_lisaa_negatiivista(self):
        self.assertIsNone(self.varasto.lisaa_varastoon(-1))

    def test_lisays_muuttaa_saldoksi_korkeintaan_tilavuuden(self):
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_ota_maara_ei_ole_negatiivinen(self):
        self.assertAlmostEqual(self.varasto.ota_varastosta(-1), 0.0)

    def test_ota_antaa_kaiken_varastosta(self):
        self.varasto.lisaa_varastoon(5)
        self.assertAlmostEqual(self.varasto.ota_varastosta(10), 5)

    def test_ota_antaa_kaiken_ja_tyhjentaa_varaston(self):
        self.varasto.lisaa_varastoon(5)
        self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)

    def test_str_palauttaa_oikean_merkkijonon(self):
        self.assertAlmostEqual(self.varasto.__str__(), "saldo = 0, vielä tilaa 10")
    

    