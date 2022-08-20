# Build CarModel and CarMake Django Models
A dealership typically manages cars from one or more makes, and customers should be allowed to review the cars they purchased from a dealer.

In this lab, you will create the car model and car make related models in the Django app.

*   A car model includes basic information such as its make, year, type, and dealer id.
*   A car make  includes basic information such as name and description.


# To Build Car Model and Car Make models
You will need to create two new models in `djangoapp/models.py`:
*   A `CarMake` model to save some data about a car make.
*   A `CarModel` model to save some data about a car model.

You could find some hints in the code comments with the tag `<HINT>`.
*   Create a car make Django model `class CarMake(models.Model):`:
    *   Name
    *   Description
    *   Any other fields you would like to include in a car make
    *   A `__str__` method to print a car make object

*   Create a car model Django model `class CarModel(models.Model)`:
    *   Many-To-One relationship to `CarMake` model (One car make has many car models, using a ForeignKey field)
    *   Dealer Id (IntegerField) refers to a dealer created in Cloudant database
    *   Name
    *   Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, and WAGON)
    *   Year (DateField)
    *   Any other fields you would like to include in a car model
    *   A `__str__` method to print the car model object

*   Run migrations for the models.
python3 manage.py makemigrations onlinecourse && python3 manage.py migrate

Refer to the previous Django ORM lab for more details:
<a href="https://cocl.us/8Z1B5?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMCD0321ENSkillsNetwork23970854-2022-01-01" target="_blank">CRUD on Django Model Objects</a>


# To register CarMake and CarModel models with the admin site
*   First, you need to have a superuser for the admin site, if not created before.
Please use `root` as user name and `root` as password for your reviewer to login your app.

*   You need to register the `CarMake` and `CarModel` in the admin site so you can conveniently
manage their content (i.e., perform CRUD operations).

*   You will also need to create `CarModelInline` so that you could manage `CarModel` and `CarMake`
together on one page in the Admin site.

Note that for the dealer id field, you need to enter the integer dealer id you created in IBM Cloudant database.
So that the car model can be associated with a dealer in the Cloudant database.

*   After you register the new models, you can create a new car make with several cars for testing.
Refer to the previous Admin site lab for more details:
<a href="https://cocl.us/TzAvw?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMCD0321ENSkillsNetwork23970854-2022-01-01" target="_blank">Django Admin Site</a>
