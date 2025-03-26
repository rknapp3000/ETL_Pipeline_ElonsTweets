
import dagster as dg

twitter_etl_job = dg.define_asset_job(
    name="twitter_etl_job",
    selection=dg.AssetSelection.all()
)
