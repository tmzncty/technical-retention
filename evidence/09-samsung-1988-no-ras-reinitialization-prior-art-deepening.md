# Case 09 — Samsung 1988 no-RAS reinitialization

Samsung Semiconductor's 1988 *MOS Memory Data Book* moves the bounded product-document floor for the no-RAS reinitialization relation to at least 1988. KM4164B pairs a 2 ms refresh requirement with eight initialization cycles after 2 ms without RAS. KM41256A/KM41257A pairs a 4 ms requirement with explicit CBR counter refresh, a separate counter-test initialization, and eight general cycles after 4 ms without RAS.

Engineering boundary: general no-RAS reinitialization is not proof of a CBR-counter-specific cause; equal eight-cycle counts do not prove identical hidden-state semantics. Samsung's wording is weaker than Hyundai/Mosel's explicit continuous-bias wording. Case 09 remains `grounded`.