from sqlalchemy import func, distinct

from ssi.db import db


class Moe(db.Model):
    __tablename__ = 'moe'

    id = db.Column('id', db.Integer(), primary_key=True)
    pdb = db.Column('PDB', db.String(120))
    type = db.Column('Type', db.String(120))
    cb = db.Column('cb.cb', db.Float())
    sc = db.Column('sc_.exp_avg', db.Float())
    hb_energy = db.Column('hb_energy', db.Float())
    residue_1 = db.Column('Residue.1', db.String(120))
    residue_2 = db.Column('Residue.2', db.String(120))
    chain_id = db.Column('chainId', db.String(120))
    expression_host = db.Column('expressionHost', db.String(1000))
    source = db.Column('source', db.String(1000))
    resolution = db.Column('refinementResolution', db.Float())
    avg_b_factor = db.Column('averageBFactor', db.Float())
    chain_length = db.Column('chainLength', db.Integer())
    ligand_id = db.Column('ligandId', db.String(120))
    het_id = db.Column('hetId', db.String(120))
    residue_count = db.Column('residueCount', db.Integer())

    def to_map(self):
        return {
            "id": self.id,
            "PDB": self.pdb,
            "Type": self.type,
            "cb.cb": self.cb,
            "sc_.exp_avg": self.sc,
            "hb_energy": self.hb_energy,
            "Residue.1": self.residue_1,
            "Residue.2": self.residue_2,
            "chainId": self.chain_id,
            "expressionHost": self.expression_host,
            "source": self.source,
            "refinementResolution": self.resolution,
            "averageBFactor": self.avg_b_factor,
            "chainLength": self.avg_b_factor,
            "ligandId": self.ligand_id,
            "hetId": self.het_id,
            "residueCount": self.residue_count
        }


def get_all_by_pdb(pdb):
    query = db.session.query(Moe) \
        .filter(Moe.pdb == pdb)
    return query


def get_hbond_counts():
    query = db.session.query(Moe.pdb, func.count(distinct(Moe.cb))) \
        .group_by(Moe.pdb)
    return query


def get_hbond_type_counts():
    query_string = 'SELECT "PDB", "Type", count(distinct ("Type", "cb.cb")) ' \
                   'FROM moe GROUP BY "PDB", "Type"'
    query = db.engine.execute(query_string)
    return query


def get_data_from_filters(filter_string):
    query_string = """
    SELECT
        "PDB",
        count(DISTINCT "cb.cb") as "hbonds",
        "chainLength" as "residues",
        count(DISTINCT "cb.cb") / CAST("chainLength" AS FLOAT) AS "hbonds/residues",
        "refinementResolution" as "resolution"
    FROM
        moe
    WHERE
        %s
    GROUP BY
        "PDB",
        "refinementResolution",
        "chainLength"
    """
    return db.engine.execute(query_string % filter_string)


def get_residue_data_from_filters(filter_string):
    query_string = """
    SELECT
        "PDB",
        count(DISTINCT ("PDB", "cb.cb", 
            substring("Residue.1", 6, 3), substring("Residue.2", 6, 3))) AS "hbonds",
        "chainLength" AS "residues",
        count(DISTINCT ("PDB", "cb.cb", 
            substring("Residue.1", 6, 3), substring("Residue.2", 6, 3))) 
                / CAST("chainLength" AS FLOAT) AS "hbonds/residues",
        "refinementResolution" AS "resolution"
    FROM
        moe
    WHERE 
        %s
    GROUP BY
        "PDB",
        "refinementResolution",
        "chainLength";
    """
    return db.engine.execute(query_string % filter_string)
