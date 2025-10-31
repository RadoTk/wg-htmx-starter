from decimal import Decimal
from django.core.files.base import ContentFile
from wagtail.images.models import Image
from wagtail.models import Page
from django.db import models

parent = Page.objects.filter(depth=2).first()

gif_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x00\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B'
image_file = ContentFile(gif_data, name='test.gif')
img = Image(title="Test Image", file=image_file)
img.save()

def create_test_product_model(on_delete_behavior):
    class TestProduct(Page):
        image = models.ForeignKey(
            "wagtailimages.Image",
            on_delete=on_delete_behavior,
            null=True,
            blank=True,
            related_name="+",
        )
        price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("9.99"))

        parent_page_types = [Page]
        subpage_types = []

        class Meta:
            app_label = 'store'

    return TestProduct

behaviors = {
    "CASCADE": models.CASCADE,
    "SET_NULL": models.SET_NULL,
    "PROTECT": models.PROTECT,
    "DO_NOTHING": models.DO_NOTHING,
}

for name, behavior in behaviors.items():
    TestProductTemp = create_test_product_model(behavior)
    product = TestProductTemp(title=f"Test {name}", image=img)
    parent.add_child(instance=product)
    product.save_revision().publish()

    print(f"\n=== Test {name} ===")
    try:
        img.delete()
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")

    try:
        product.refresh_from_db()
        print("Produit après suppression :", product)
        print("Image du produit :", product.image)
    except TestProductTemp.DoesNotExist:
        print("Le produit a été supprimé (CASCADE)")

    img = Image(title="Test Image", file=image_file)
    img.save()
