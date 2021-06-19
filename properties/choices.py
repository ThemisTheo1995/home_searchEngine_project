from django.utils.translation import ugettext_lazy as _

price_sale_choices = {
  '100000':'$100,000',
  '200000':'$200,000',
  '300000':'$300,000',
  '400000':'$400,000',
  '500000':'$500,000',
  '600000':'$600,000',
  '700000':'$700,000',
  '800000':'$800,000',
  '900000':'$900,000',
  '1000000':'$1M+',
}

price_rent_choices = {
  '100':'100€',
  '200':'200€',
  '300':'300€',
  '400':'400€',
  '500':'500€',
  '600':'600€',
  '700':'700€',
  '800':'800€',
  '900':'900€',
  '1000':'1000€',
  '1200':'1200€',
  '1500':'1500€',
  '2000':'2000€',
  '2500':'2500€',
  '3000':'3000€',
  '5000':'5000€',
}

type_rent_choices = {
  'Flat/Apartment':'Flat/Apartment',
  'Cottage':'Cottage',
  'Detached':'Detached',
  'Semi-Detached':'Semi-Detached',
  'Terraced':'Terraced',
  'Studio':'Studio',
  'Bungalow':'Bungalow',
  'Penthouse':'Penthouse',
  'Land':'Land',
  'Shared':'Shared',
}

furniture_choices = {
  'Furnished':'Furnished',
  'Unfurnished':'Unfurnished',
}

order_list_date_choices = {
  'old':_('Oldest listed'),
  'new':_('Newest listed'),
}

order_price_choices = {
  'high':_('Highest price 🠗'),
  'low':_('Lowest price 🠕'),
}

pagination_choices = {
  '15':'15',
  '20':'20',
  '30':'30',
  '50':'50',
}