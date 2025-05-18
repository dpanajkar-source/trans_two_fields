class Settings:
    # Key mappings for simple transformations
    mappings = {
        "total_net_worth": "totalNetWorth",
        "total_plan_current_assets": "totalPlanCurrentAssets",
        "total_plan_current_liabilities": "totalPlanCurrentLiabilities"
    }

    # Comprehensive mapping dictionary
    mapping_dictionary = {
        "package_id": None,  # From UI or generator
        "eci": None,  # From UI or generator
        "total_net_worth": "totalNetWorth",  # From networth API
        "total_plan_current_assets": "totalPlanCurrentAssets",  # From networth API
        "total_plan_current_liabilities": "totalPlanCurrentLiabilities",  # From networth API
        "plan_updated_by": "updateUserIdentifier",
        "plan_updated_date": "updateTimestamp",
        "plan_created_on_date": "createTimestamp",
        "plan_created_by": "createUserIdentifier",
        "goal_attributes": [
            {
                "goal_id": "analysisGoals.analysisGoalId",
                "goal_name": "analysisGoals.goalName",
                "goal_type": "analysisGoals.goalType",
                "goal_rank": "analysisGoals.goalRank",
                "goal_owner": "scenariosList.goals.owners",
                "goal_frequency_type_code": "scenariosList.goals.frequencyTypeCode",
                "goal_frequency_number_of_years": "scenariosList.goals.frequencyNumberOfYears",
                "bucket_to_goal_relationship": "scenariosList.goals.analysisBucketId",
                "bucket_name": "analysisBuckets.analysisBucketName",
                "estimated_goal_amount": None,
                "goal_periods": [
                    {
                        "goal_period_id": "scenariosList.goals.goalPeriods.goalPeriodId",
                        "start_year_number": "scenariosList.goals.goalPeriods.startYearNumber",
                        "end_year_number": "scenariosList.goals.goalPeriods.endYearNumber",
                        "annual_amount": "scenariosList.goals.goalPeriods.annualAmount",
                        "monthly_amount": "scenariosList.goals.goalPeriods.monthlyAmount",
                    }
                ],
                "participants": [
                    {
                        "analysis_participant_id": "participants.analysisParticipantId",
                        "electronic_client_id": "participants.electronicClientId",
                        "party_relationship_code": "participants.partyRelationshipCode",
                        "marital_status_name": "participants.maritalStatusName",
                        "applicant_employment_type": "participants.applicantEmploymentType",
                        "first_name": "participants.firstName",
                        "full_name": "participants.fullName",
                        "income_amount": "participants.incomeAmount",
                        "date_of_birth": "participants.dateOfBirth",
                        "life_expectancy_number": "participants.lifeExpectancyNumber",
                        "retirement_age_number": "participants.retirementAgeNumber",
                        "social_security_distribution_age_number": "participants.socialSecurityDistributionAgeNumber",
                        "social_security_receive_status_code": "participants.socialSecurityReceiveStatusCode",
                        "social_security_strategy_type_code": "participants.socialSecurityStrategyTypeCode",
                        "residency_periods": [
                            {
                                "start_year_number": "participants.residencyPeriods.startYearNumber",
                                "end_year_number": "participants.residencyPeriods.endYearNumber",
                                "address_state_code": "participants.residencyPeriods.addressStateCode",
                            }
                        ]
                    }
                ],
                "portfolio": [
                    {
                        "portfolio_id": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.portfolioId",
                        "portfolio_name": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.name",
                        "portfolio_type": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.type",
                        "portfolio_allocs": [
                            {
                                "cma_id": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.allocs.cmaId",
                                "asset_class_name": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.allocs.assetClassName",
                                "amount": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.allocs.amount",
                                "percent": "scenariosList.goalFeasibilityResponse.plan.portfoliosClient.allocs.percent",
                            }
                        ]
                    }
                ]
            }
        ]
    }
