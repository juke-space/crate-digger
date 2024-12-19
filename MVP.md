# Minimum Viable Product
A high-level description of what we are building, why we are building it, and what the minimally viably version of that solution looks like.

## What is it we are building? What problem are solving?
### Streaming vs. Search



## Customer pain points
* Forced to rely on automated algorithms for music search and discovery, with little to no input
* Often given "poor" recommendations from automated recommendation systems
* Often given repeated recommendations
* Often get biased recommendations based on previous likes/dislikes that are difficult to change

## Competitive landscape
* Primarily automated recommendation systems, of which there are many (big) players

## Implementation ideas (remove ones we aren't keeping after we discuss them)
| Type      | Idea        |
| --------- | ----------- |
| Interface | Desktop app | 
| Interface | Single line of interface discussed and put in discord (Find 'entity' with 'condition' as 'value') |
| Interface | Only 'Blast off!!!' button from interface in discord (if going with idea above since only one coordinate) |
| Interface | Simple 'list of items' for results page |
| Interface | Item in list on results page contains link to song in Spotify (opens in Spotify if installed on PC) |
| Feature   | 'Song' and 'Artist' for entities |
| Feature   | 'Genre' and 'Where it's made' Conditions for 'Song' entity |
| Feature   | 'Worked with' and 'From' Conditions for 'Artist' entity |
| Monetary  | 'Support us' button with link to Patreon, Buy me a coffee, etc. |

### Notes
- Start with a web application.
- Start with just a search engine for artists
- Start simple - python backend, some sort of js or htmx frontend, sqlite database.
- Deploy simply, rpi with Argo Tunnel via CloudFlare (no port-forwarding, no subscription)
- Search must be able to go beyond artist by name
- Playback may be available, but is not a priority

## Validity test 
- [ ] Ready for launch?

Add anyone you know who would be open to testing the MVP after it's built, but before released to customers:

| Tester       | Feedback                           | 
| ------------ | ---------------------------------- |
| Alex M       |
| Chris M      |
| Tyce B       |
| Gavin C      |
| Gwen F       |
| Rob F        |
| Lydia A      |
| Jaedon B     |
| Nick K       |
| Cam H        |
| Erik W       |
| Read W       |

  
## Reference(s)
* https://www.atlassian.com/agile/product-management/minimum-viable-product
* https://theleanstartup.com/principles
* https://link.springer.com/article/10.1007/s13735-018-0154-2
