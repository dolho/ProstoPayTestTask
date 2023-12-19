# Test task for Middle Python Developer  

To run the tests simply call `docker compose up`

To assert the same style of the code `black`, `mypy` and `isort` 
linters were used. 

### Hashmap implementation notes

For the implementation of the Hashmap data structure, 
a generic solution was chosen, involving the storage of data in lists (in a more low-level languages an array would be chosen instead). 
Although other alternatives such as various tree structures 
(e.g., prefix tree, radix tree) might be more efficient for specific use cases, 
the decision was made to go with a more generalized approach.

To address collisions, a separate chaining collision resolution method was implemented due to its simplicity. 
Other alternatives, such as different probing methods (with linear probing being the simplest), were considered but not adopted in favor of simplicity.

The implementation has been thoroughly tested, covering both positive and negative test cases to ensure its robustness.

### UserHandler implementation notes
A straightforward implementation with the aim of minimizing duplicating
lines of code when transforming a Pydantic model into a SQLAlchemy model and vice versa.

To test the implementation a postgresql db was added to the docker compose and 
testing infrastructure (like factories, db connections et ce tera) was added.