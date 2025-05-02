from .locations import (RegionModelTest, DistrictModelTest, ModelTranslationTest,
                        RegionAPITest, RegionPermissionsTest, DistrictAPITest, LanguageAPITest)

from .academic_degrees import (AcademicDegreeModelTest, AcademicDegreeSerializerTest, 
                               AcademicDegreeViewSetTest)

from .subscriptions import (AdvantageModelTest, SubscriptionModelTest,
                            SubscriptionAdvantageRelationshipTest, ModelTranslationTest,
                            SubscriptionSerializerTest, SubscriptionViewSetTest, SubscriptionAPIIntegrationTest)

from .specialties import (SpecialtyModelTest, SpecialtySerializerTest, SpecialtyViewSetTest, 
                          SpecialtyAdminAPITest, SpecialtyAdminPermissionTest)

from .medical_categories import (MedicalCategoryModelTest, MedicalCategorySerializerTest, MedicalCategoryViewSetTest)

from .services import (ServiceModelTest, ServicePlaceModelTest, ServiceSerializerTest, ServiceViewSetTest)

from .languages import (LanguageModelTest, LanguageLevelModelTest, LanguageSerializerTest, LanguageLevelSerializerTest)

from .experience_levels import (ExperienceLevelModelTest, ExperienceLevelSerializerTest, ExperienceLevelViewSetTest)

from .social_statuses import (SocialStatusModelTest,)