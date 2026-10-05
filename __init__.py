from src.scrapers.cheo import CheoScraper
from src.scrapers.ottawa_hospital import OttawaHospitalScraper
from src.scrapers.royal import RoyalScraper
from src.scrapers.tribe import TribeMedicalScraper
from src.scrapers.invita import InvitaScraper


SCRAPERS = {
    "CHEO": CheoScraper,
    "The Ottawa Hospital": OttawaHospitalScraper,
    "The Royal": RoyalScraper,
    "Tribe Medical": TribeMedicalScraper,
    "InVita Healthcare Technologies": InvitaScraper,
}
