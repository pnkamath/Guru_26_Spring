--[[
Because we are passing a payload that contains the queue of events,
we gain a really powerful new ability: the FSM can modify its own
future. If the character takes a hit and their HP drops below 0,
the FSM can dynamically inject a "die" event to the very front of
the queue, instantly hijacking the flow.

You don't need to change the engine from the previous step at all.
You just need this main.lua:
]]
--
local machine = require("fsm3")

-- 1. Define the rules, actions, and transitions
local rpg_rules = {
	idle = {
		action = function(p)
			print("\n[" .. p.name .. "] is idling. HP: " .. p.hp)
		end,
		transitions = { walk = "moving", attack = "attacking", hit = "staggered", die = "dead" },
	},

	moving = {
		action = function(p)
			print("[" .. p.name .. "] is walking forward.")
		end,
		transitions = { stop = "idle", attack = "attacking", hit = "staggered", die = "dead" },
	},

	attacking = {
		action = function(p)
			print("[" .. p.name .. "] swings their weapon!")
		end,
		transitions = { recover = "idle", hit = "staggered", die = "dead" },
	},

	staggered = {
		action = function(p)
			-- Pull the next damage amount from our payload's separate damage queue
			local dmg = table.remove(p.damage_queue, 1) or 0
			p.hp = p.hp - dmg
			print("   > BOOM! [" .. p.name .. "] took " .. dmg .. " damage! HP is now " .. p.hp)

			-- If HP drops below 0, the FSM modifies its own memory to force a death state next
			if p.hp <= 0 then
				print("   > SYSTEM: Fatal damage detected! Injecting 'die' event...")
				table.insert(p.queue, 1, "die") -- Insert at the front of the queue
			end
		end,
		transitions = { recover = "idle", die = "dead" },
	},

	dead = {
		action = function(p)
			print("[" .. p.name .. "] has collapsed to the ground.")
		end,
		transitions = { revive = "idle" },
	},
}

-- 2. Define the payload (Memory + Queues)
local my_payload = {
	name = "Hero",
	hp = 100,
	-- The sequence of events we want the FSM to process
	queue = {
		"walk",
		"attack",
		"recover",
		"hit",
		"recover",
		"walk",
		"attack",
		"hit",
		"walk", -- Note: They will die on this second hit, so the final "walk" will be ignored!
	},
	-- A custom queue just for this payload to hold damage amounts
	damage_queue = { 15, 90 },
}

if arg[1] == "--dot" then
	print(machine.to_dot(rpg_rules))
	os.exit()
end

print("=== STARTING TCO RPG BATTLE ===")

-- Boot up the machine! (Passing the rules, initial state, and payload memory)
local final_memory = machine.start(rpg_rules, "idle", my_payload)

print("\n=== PROCESSING COMPLETE ===")
print("Final Queue Size remaining: " .. #final_memory.queue)
print("Final HP: " .. final_memory.hp)
