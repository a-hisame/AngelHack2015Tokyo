# API List

## Basic Rules

* ContextRoot: hungry
* Single HTML URL: /[ContextRoot]/[Accesser]
* API HTML URL: /[ContextRoot]/api/[Accesser]

## URLs

### pages

* /[ContextRoot]: index page
* /[ContextRoot]/index: index page
* /[ContextRoot]/upload: upload example form

### APIs

#### Implemented

* /[ContextRoot]/api/suggest?keyword=: suggestion combines name and tags
* /[ContextRoot]/api/suggest/name?keyword=: suggestion name
* /[ContextRoot]/api/suggest/tag?keyword=: suggestion tag
* /[ContextRoot]/api/search/dishes?keyword=: search registed dishes (keyword can be separated the ",")
* /[ContextRoot]/api/search/restaurant?keyword=: search registed restaurant list
* /[ContextRoot]/api/restaurant?name=: get information of single restaurant which name matched
* /[ContextRoot]/api/upload: upload dishes information (see pages upload form paramters)


#### Not Implemented

* /[ContextRoot]/api/dish?name=: get information of single dish which name matched
* /[ContextRoot]/api/suggest/restaurang?keyword: suggestion restaurant


