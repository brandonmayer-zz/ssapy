SSAPY - Simultaneous Second-price Auction PYthon module
=======================================================

Originally written for CSCI2951, *"[Autonomous Agents and Computational Market Design](http://www.cs.brown.edu/courses/csci2951-c/)"*
with Professor Amy Greenwald, and TA Eric Sodomka in the Computer Science Department at Brown University.

Algorithms and Data are separated as much as possible. To that end, ssapy.strategies implements heuristics as callable functions.
Each strategy takes as input an arbitrary revenue function and price prediction and therefore can be used in any game specification.
"Agents" encapsulate the state of individuals bidding in specific games. Agents use strategies and their current state to place bids.

ssapy.agents is the home for agents. For all game types there should be a corresponding agent module. For example ssapy.agents.marketSchedule
implements agents for the market scheduling game described in [Yoon11] and [Reeves05]. All agents should inherit from ssapy.agents.agentBase class which assigns 
each agent a unique id (just an integer - maybe change to a uuid.uuid4()?) at the beginning of the simulation.

All agents implement a bid(**kwargs) function which returns the bid placed by the agent either given arguments to the function or based
soley on the current state of the agent.

References:

 1. [Wellman11] Wellman, M.P. (2011). "Trading Agents". Morgan & Claypool Publishers   

 1. [Yoon11] Yoon, D.Y., & Wellman, P.M.(2011). "Self-Confirming Price Prediction for Bidding in Simultaneous Second Price Sealed Bid Auctions". The 2011 Workshop on Trading Agent Design and Analysis. Barcelona, Catalonia, Spain.   

 3. [Reeves05] Reeves, Wellman, MacKie-Mason, Osepayshvili (2005). "Exploring bidding strategies for market-based scheduling" Decision Support Systems.