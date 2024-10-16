# MILP modeling the search for MITM preimage attack on weakened Camellia

This folder provides source codes as follows: 

* `Configration.py` is used to pre-define the parameters associated with the algorithm. 
* `utils.py` encapsulates some common tool methods. 
  * `BasicTools class` encapsulates some common constraint expression methods, such as variables addition`plusTerms(in_vars)`, variables subtraction`minusTerms(in_vars)`, etc.
  * `MITMPreConstraints class` encapsulates a number of constraint expressions that have some relevance to the algorithm.
* `SupP_Camellia_mitm.py` is for generating MILP models searching for MITM preimage attack on weakened Camellia.
  * `Vars_generator class` encapsulates the variable definitions associated with the MILP model. 
  * `Constraints_generator class` declares the specific methods for generating constraints for each component of the algorithm.

For this project, We only need to run the main function of `SupP_Camellia_mitm.py` to generate the MILP model and solve it.