STATE    <-      ACTIONS
      -> VIEW ->


Parent -> Child
  Data through props

Child -> Parent
  - Pass info through events
  - Directly invoke parents methods/modify data
      - HARD TO DEBUG
      - AVOID 



Multiple views derived from same peice of state
Mulitple components can update this piece

Sibling Components
  - Same / Similar Level [have one common ancestor]
  - Pass event up to the common node
  - State changes
  - Data passed as props to sibling

Global Variables ??
-> Modifiable by all components
-> Difficult to track who modified / debug



COMPROMISE

-> Gloabl state BUT
-> Changes constrained
  - No direct modification
  - Only through specifu mutations

vuex




Which of the following statements is true for VueJS?
- Vue provides a progressive framework, i.e. it can be easily used to integrate with an existing project and is incrementally adoptable.
- The SFC (Single File Components) makes it easy to create an SPA.
- Vue Routers helps in creating SPAs.

