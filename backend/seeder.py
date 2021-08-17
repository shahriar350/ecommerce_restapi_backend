from django_seed import Seed

seeder = Seed.seeder('en_EN')

from admin_app.models import ProductVariationAdmin, ShopCategory, Category


seeder.add_entity(ProductVariationAdmin, 10)
seeder.add_entity(ShopCategory, 10)
seeder.add_entity(Category, 10)

inserted_pks = seeder.execute()
