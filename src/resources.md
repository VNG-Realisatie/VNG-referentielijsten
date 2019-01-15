# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## CommunicatieKanaal

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/communicatiekanaal)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| naam | De gangbare naam van het communicatiekanaal. | string | ja | C​R​U​D |
| omschrijving | Toelichtende beschrijving van (de naam van) het communicatiekanaal. | string | ja | C​R​U​D |

## ProcesType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/procestype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Nummer van de selectielijstcategorie | integer | ja | C​R​U​D |
| naam | Benaming van het procestype | string | ja | C​R​U​D |
| omschrijving | Omschrijving van het procestype | string | ja | C​R​U​D |
| toelichting | Toelichting van het procestype | string | ja | C​R​U​D |
| procesobject | Object waar de uitvoering van het proces op van toepassing is en waarvan de bestaans- of geldigheidsduur eventueel van belang is bij het bepalen van de start van de bewaartermijn | string | ja | C​R​U​D |


* Create, Read, Update, Delete
