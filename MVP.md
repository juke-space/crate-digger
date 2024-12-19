# Minimum Viable Product
A high-level description of what we are building, why we are building it, and what the minimally viably version of that solution looks like.

## What is it we are building? What problem are solving?

For an in-depth description of the problem see: https://theluddite.org/post/the-playlist-lie.html

### Streaming vs. Search

- If someone wants to play music on the internet, there are many, many good options for that
- There is not a good solution for exploring music space
- Exploring music space is more than just playing unheard music or receiving / listening to recommendations.
- An **exploration**, speaking in terms of a literal expedition, has some *direction*
- If we are to build a search engine that is not just a vehicle for record finding, but music exploration,
    we ought to focus on aiding the user in heading the direction they are trying to head in
- More broadly, we want to bring out the *intention* behind a users search and facilitate an exploration of that kind.
- We ought to focus on building a tool that allows you to land in a certain location, generally, and then traverse the landscape to find what is of interest.
- It is less important that the "search" provides the exact "coordinates" (i.e. specific song or artist) that you are interested in.
    - see https://music-map.com, searching a particular artist gives you is a sea of other artists.
- This makes interactivity as well as more intimate control over the exploration landscape provided required for a good user experience.
- Once we have the search and exploration portion solidified, we should try and add a social component to this (as we have previously discussed). Not important for an MVP.

## Customer pain points
* Forced to rely on automated algorithms for music search and discovery, with little to no input
* Often given "poor" recommendations from automated recommendation systems
* Often given repeated recommendations
* Often get biased recommendations based on previous likes/dislikes that are difficult to change
* Complexity of the music landscape is summarized so generally it is hard to understand the terrain (i.e. overly-smooth)

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
- Results should be visual (more than just a list?)

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
### Product Inspiration
* https://www.music-map.com/
* https://everynoise.com/
* https://listenbrainz.org/
### Process Inspiration
* https://www.atlassian.com/agile/product-management/minimum-viable-product
* https://theleanstartup.com/principles
* https://link.springer.com/article/10.1007/s13735-018-0154-2
