from pydantic import BaseModel, Field


class RatingsDistribution(BaseModel):
    ratingOne: int
    ratingTwo: int
    ratingThree: int
    ratingFour: int
    ratingFive: int


class OverviewData(BaseModel):
    total: int
    average: float
    ratingsDistribution: RatingsDistribution


class StatsOverviewResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Overview sobre os dados.")
    data: OverviewData = Field(
        ...,
        example={
            "total": 100,
            "average": 15.99,
            "ratingsDistribution": {
                "ratingOne": 10,
                "ratingTwo": 20,
                "ratingThree": 30,
                "ratingFour": 25,
                "ratingFive": 15
            }
        }
    )
