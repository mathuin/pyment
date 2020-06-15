User's guide
============

The purpose of this document is to walk the mead maker through all the
major operations required to use the software.  Throughout this
document, this role is referred to as the producer.  This is in
contrast to the consumer, who plays a significant role in the
distribution section.

Setup
-----

``pyment`` is like any other Django app in that it must be deployed in
order to be useful.  Deployment specifics are beyond the scope of this
document, but references such as `How to deploy with WSGI
<https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/>`_ and
tutorials such as `How To Deploy a Local Django App to a VPS
<https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps>`_
are available on the internet.  At the very minimum, the producer will
need a Django user account in order to access the admin site to
perform many of the operations listed below.  For more information
about the admin site, including how to use it, please see `Chapter 6:
The Django Admin Site
<http://www.djangobook.com/en/2.0/chapter06.html>`_.

Production
----------

.. warning:: It is essential to remember that there are many ways to
	     brew mead, and that this software was written to suit the
	     particular brewing :doc:`process <brewprocess>` used by
	     its author.  That being said, other brewers will likely
	     find this software useful, and :doc:`pull requests <dev>`
	     are cheerfully encouraged.

This section focuses on the basics of mead production: ingredients,
recipes, batches, and products.  A discussion of samples is also
included.

Ingredients
~~~~~~~~~~~

Ingredients are the raw components of the mead.

There are four types of ingredients:

* sugars (example: wildflower honey)
* solvents (example: spring water)
* flavors (example: bulk cinnamon)
* yeasts (example: Red Star champagne yeast)

Different types of information are stored for each type of ingredient:

* Specific gravity and specific heat (sugars and solvents)
* Cost per unit (all)
* "Natural" or not (all but yeast)
* Appellation (all but yeast)

Cost per unit is recorded per kilogram for sugars, per liter for
solvents, "other" for flavor, and per packet or vial for yeast.
"Natural" is defined as "does not contain added color, artificial
flavors or synthetic substances" for these purposes.  Appellation
describes the region from which the ingredient is sourced.

Ingredients are created from the ingredient select page and can be
changed at the ingredient change page.

Recipes
~~~~~~~

Recipes are collections of ingredients, including the ingredient's
amount and (in the case of sugars and solvents) temperature as
appropriate.  The total cost of the batch can be calculated based on
the ingredients and their amounts.

Information for the ingredients is also used to determine the
appropriate BJCP category.  Here are some examples:

* A recipe with apple juice as the only solvent will be classified as
  a cyser.

* A recipe with spices as the only flavor will be classified as a
  metheglin.

* A recipe with apple juice *and* spices will be classified as an open
  category mead.

.. note:: These classifications are just recommendations.  If they are
          incorrect or incomplete, please submit :doc:`bug reports
          <bugfeature>` as appropriate.

Recipes also have titles and descriptions for organizational purposes
as well.

Recipes can be created from the recipe select page as well as from
existing batches by pressing the "Create recipe from batch" button on
the batch's change page.

Batches
~~~~~~~

Batches are actual instantiations of recipes.  Sometimes brew day
doesn't go exactly as planned, so ingredient substitutions and other
changes are possible.  Additionally, samples are associated with
batches.

Like recipes, batches have titles and descriptions.  Unlike recipes,
batches also have names.  Batch names are composed of unique strings
representing brewing events and a batch letter indicating the sequence
in which the batch was brewed.  The author uses batch names like "SIP
26 C", where "SIP 26" represents the brewing event and "C" indicates
that this was the third batch brewed during that event.  Any non-empty
string can be used as an event identifier.

Batches can be created from the recipe's change page by pressing the
'Create batch from recipe' button.  Placeholder values for the
batch-specific information must be changed immediately to avoid
conflict with other batches.

.. todo:: In the future, pressing this button will result in a dialog
          box requesting user input for these values.

Products
~~~~~~~~

Products are batches which have been bottled.  Once the bottling is
complete, labels can be generated based on the product's ingredients
and other characteristics.  Jars of products that have been labeled
can be entered into the inventory management system.

Product names, titles, and descriptions are all inherited from their
batches.  Product titles and descriptions are currently used for both
labels and distribution.

When a batch is bottled into jars, the Jars field of the batch's
change page must be updated and the batch saved.  At this point labels
can be printed and applied to the jars.  A product can then be created
from that batch by pressing the "Create product from batch" button on
the batch's change page.

Samples
~~~~~~~

Samples are taken throughout the lifetime of the batch.  The following
information is collected for each sample:

* Temperature (in degrees Fahrenheit)
* Specific gravity
* Notes (traditionally used for sensory data)

These samples are used to calculate the percent alcohol of the mead,
and are convenient for storing information which can be referenced
when making labels.

Storage
-------

Once the mead is produced, it must be stored in such a manner as to
facilitate easy retrieval of specific jars.  This requires an
inventory management system (IMS).  The largest unit of storage in the
IMS is the warehouse.  Each warehouse is a collection of rows.  Each
row is a collection of shelves.  Each shelf is a collection of
crate-sized bins.  Each bin contains one or more crates.  Each crate
contains one or more jars.  At least one bin and one crate must be
created for the IMS to function.

Create jars
~~~~~~~~~~~

Jar creation is done by running a Django management command.  This
requires logging into the production server and activating a virtual
environment if appropriate.  Here is an example::

  (venv)# python manage.py add_new_jars --product="SIP 26 C" --start-jar=1 --end-jar=12 --crate=37
  12 jars were created in SIP 26 C and placed in Crate 37

The crate must exist and must have sufficient capacity to contain the
jars for this command to succeed.  At this point the jars are now
available for distribution.

.. note:: If the producer wishes to protect a jar from being
          distributed, they should use the admin interface to set that
          jar's "is available" flag to False.

Crate consolidation
~~~~~~~~~~~~~~~~~~~

As jars are removed from the IMS, crates will become less full.
Partially full crates will need to be consolidated in order to make
empty crates available for new product.  Candidates for crate
consolidation can be identified by running a Django management
command.  Here is an example::

  (venv)# python manage.py crate_utilization --warehouse=2
  Crate ID |         Bin         | Capacity | Jars
  ==================================================
     21    | Row 1 Shelf 2 Bin 2 |    12    |  5
     39    | Row 1 Shelf 2 Bin 2 |    12    |  5
     44    | Row 2 Shelf 2 Bin 2 |    12    |  6
     32    | Row 1 Shelf 1 Bin 2 |    11    |  6
     33    | Row 1 Shelf 1 Bin 1 |    11    |  6

A number of crates in this example can be consolidated.  To transfer
all the jars from crate 21 to crate 32, use the following command::

  (venv)# python manage.py crate_transfer --source=21 --dest=32
  5 jars were moved from Crate 21 to Crate 32

Crate 21 is now considered empty and can be used for new product.

Distribution
------------

This section introduces a new role: the consumer, the person who
actually orders and consumes the mead.  Typically, the producer and
the consumer are both the same person who also made the mead in
question.  However, each role performs different actions in this
section.

Order placement
~~~~~~~~~~~~~~~

The order placement process is similar to that in any other store on
the web.

#. (Optional) Accounts can be created by consumers, including
   information such as email address and phone number.

#. The consumer selects a product, modifies the quantity if
   appropriate, and presses the "Add To Cart" button, repeating as
   necessary.

#. The consumer presses the "Checkout" button, possibly updates
   contact info, then presses the "Place Order" button.

This causes an order to be generated, and emails to be sent to the
consumer and the producer.

Order fulfillment
~~~~~~~~~~~~~~~~~

#. The producer visits the relevant link in the email.  After
   confirming the validity of the order, the producer then presses the
   "Process order" button.  This marks the order as 'processed',
   generates a pick list and sends another email to the consumer.
   This pick list has one line for each jar in the order, including
   the name of that jar and its location (crate and bin).

#. The producer visits the pick list associated with the order.  After
   retrieving each jar identified in the pick list from the warehouse,
   the producer presses the "Process picklist" button.  This marks the
   picklist as 'processed', marks the order as 'delivered', and sends
   a final email to the consumer.

Individual orders and pick lists can also be modified and/or cancelled by
the producer.
