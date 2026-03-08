"""CPF regions according to Brazilian standards."""

from enum import IntEnum
from typing import Dict, List


class Region(IntEnum):
    """Brazilian regions for CPF issuance.
    
    The 9th digit of a CPF indicates the region where it was issued.
    """

    RIO_GRANDE_DO_SUL = 0
    CENTRO_OESTE = 1  # DF, GO, MS, MT, TO
    NORTE = 2  # AC, AM, AP, PA, RO, RR
    NORDESTE_NORTE = 3  # CE, MA, PI
    NORDESTE_LESTE = 4  # AL, PB, PE, RN
    NORDESTE_SUL = 5  # BA, SE
    MINAS_GERAIS = 6
    SUDESTE_NORTE = 7  # ES, RJ
    SAO_PAULO = 8
    SUL = 9  # PR, SC

    def get_description(self) -> str:
        """Get human-readable description of the region.
        
        Returns:
            str: Description of states in this region.
        """
        descriptions = {
            0: "Rio Grande do Sul",
            1: "Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins",
            2: "Pará – Amazonas – Acre – Amapá – Rondônia – Roraima",
            3: "Ceará – Maranhão – Piauí",
            4: "Pernambuco – Rio Grande do Norte – Paraíba – Alagoas",
            5: "Bahia – Sergipe",
            6: "Minas Gerais",
            7: "Rio de Janeiro – Espírito Santo",
            8: "São Paulo",
            9: "Paraná – Santa Catarina",
        }
        return descriptions[self.value]

    @classmethod
    def from_name(cls, name: str) -> "Region":
        """Get region from state name or abbreviation.
        
        Args:
            name: State name or abbreviation (case insensitive).
            
        Returns:
            Region: The corresponding region.
            
        Raises:
            ValueError: If state name is not recognized.
            
        Examples:
            >>> Region.from_name("SP")
            <Region.SAO_PAULO: 8>
            >>> Region.from_name("São Paulo")
            <Region.SAO_PAULO: 8>
            >>> Region.from_name("rio de janeiro")
            <Region.SUDESTE_NORTE: 7>
        """
        name_upper = name.upper().strip()
        
        # State abbreviations to region mapping
        state_map: Dict[str, Region] = {
            # Region 0
            "RS": cls.RIO_GRANDE_DO_SUL,
            "RIO GRANDE DO SUL": cls.RIO_GRANDE_DO_SUL,
            # Region 1
            "DF": cls.CENTRO_OESTE,
            "DISTRITO FEDERAL": cls.CENTRO_OESTE,
            "GO": cls.CENTRO_OESTE,
            "GOIAS": cls.CENTRO_OESTE,
            "GOIÁS": cls.CENTRO_OESTE,
            "MS": cls.CENTRO_OESTE,
            "MATO GROSSO DO SUL": cls.CENTRO_OESTE,
            "MT": cls.CENTRO_OESTE,
            "MATO GROSSO": cls.CENTRO_OESTE,
            "TO": cls.CENTRO_OESTE,
            "TOCANTINS": cls.CENTRO_OESTE,
            # Region 2
            "AC": cls.NORTE,
            "ACRE": cls.NORTE,
            "AM": cls.NORTE,
            "AMAZONAS": cls.NORTE,
            "AP": cls.NORTE,
            "AMAPA": cls.NORTE,
            "AMAPÁ": cls.NORTE,
            "PA": cls.NORTE,
            "PARA": cls.NORTE,
            "PARÁ": cls.NORTE,
            "RO": cls.NORTE,
            "RONDONIA": cls.NORTE,
            "RONDÔNIA": cls.NORTE,
            "RR": cls.NORTE,
            "RORAIMA": cls.NORTE,
            # Region 3
            "CE": cls.NORDESTE_NORTE,
            "CEARA": cls.NORDESTE_NORTE,
            "CEARÁ": cls.NORDESTE_NORTE,
            "MA": cls.NORDESTE_NORTE,
            "MARANHAO": cls.NORDESTE_NORTE,
            "MARANHÃO": cls.NORDESTE_NORTE,
            "PI": cls.NORDESTE_NORTE,
            "PIAUI": cls.NORDESTE_NORTE,
            "PIAUÍ": cls.NORDESTE_NORTE,
            # Region 4
            "AL": cls.NORDESTE_LESTE,
            "ALAGOAS": cls.NORDESTE_LESTE,
            "PB": cls.NORDESTE_LESTE,
            "PARAIBA": cls.NORDESTE_LESTE,
            "PARAÍBA": cls.NORDESTE_LESTE,
            "PE": cls.NORDESTE_LESTE,
            "PERNAMBUCO": cls.NORDESTE_LESTE,
            "RN": cls.NORDESTE_LESTE,
            "RIO GRANDE DO NORTE": cls.NORDESTE_LESTE,
            # Region 5
            "BA": cls.NORDESTE_SUL,
            "BAHIA": cls.NORDESTE_SUL,
            "SE": cls.NORDESTE_SUL,
            "SERGIPE": cls.NORDESTE_SUL,
            # Region 6
            "MG": cls.MINAS_GERAIS,
            "MINAS GERAIS": cls.MINAS_GERAIS,
            # Region 7
            "ES": cls.SUDESTE_NORTE,
            "ESPIRITO SANTO": cls.SUDESTE_NORTE,
            "ESPÍRITO SANTO": cls.SUDESTE_NORTE,
            "RJ": cls.SUDESTE_NORTE,
            "RIO DE JANEIRO": cls.SUDESTE_NORTE,
            # Region 8
            "SP": cls.SAO_PAULO,
            "SAO PAULO": cls.SAO_PAULO,
            "SÃO PAULO": cls.SAO_PAULO,
            # Region 9
            "PR": cls.SUL,
            "PARANA": cls.SUL,
            "PARANÁ": cls.SUL,
            "SC": cls.SUL,
            "SANTA CATARINA": cls.SUL,
        }
        
        if name_upper in state_map:
            return state_map[name_upper]
        
        raise ValueError(
            f"Estado não reconhecido: {name}. "
            f"Use uma sigla (ex: SP, RJ) ou nome completo do estado."
        )
