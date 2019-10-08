from .core import Dataset
import carto2gpd
import pandas as pd


class CommercialActivityLicenses(Dataset):
    """
    Load commercial activity licenses for the City of Philadelphia.

    Source
    -------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-commercial-activity-licenses
    """

    date_columns = ["issue_date"]

    @classmethod
    def download(cls):

        # todays date
        today = pd.datetime.today().strftime("%Y-%m-%d")

        # load all licenses
        carto_url = "https://phl.carto.com/api/v2/sql"
        where = f"issuedate < '{today}'"
        return (
            carto2gpd.get(carto_url, table_name="li_com_act_licenses", where=where)
            .query("legalentitytype == 'Company'")
            .drop(
                labels=[
                    "geometry",
                    "licensetype",
                    "objectid",
                    "revenuecode",
                    "legalentitytype",
                    "legalfirstname",
                    "legallastname",
                ],
                axis=1,
                errors="ignore",
            )
            .rename(
                columns=dict(
                    companyname="company_name",
                    issuedate="issue_date",
                    licensestatus="license_status",
                    licensenum="license_num",
                )
            )
            .sort_values(by="issue_date", ascending=True)
            .reset_index(drop=True)
        )

