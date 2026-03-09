--[[
Because we are passing a payload that contains the queue of events,
we gain a really powerful new ability: the FSM can modify its own
future. If the character takes a hit and their HP drops below 0,
the FSM can dynamically inject a "die" event to the very front of
the queue, instantly hijacking the flow.
]]
--
local machine = require("fsm3")

-- ─────────────────────────────────────────────
-- DSL helpers
-- ─────────────────────────────────────────────

-- FIX 1: say() — replaces "[" .. p.name .. "] " .. msg concatenation spam.
-- Supports {name}, {hp}, {dmg} placeholders so actions read like prose.
local function say(msg)
	return function(p)
		local out = msg:gsub("{(%w+)}", function(key)
			return tostring(p[key] or "")
		end)
		print(string.format("[%s] %s", p.name, out))
	end
end

-- FIX 2: merge() — shallow-merges any number of tables into a new one.
-- Used below to attach shared combat_exits to each state's transitions
-- without copy-pasting { hit = "staggered", die = "dead" } everywhere.
local function merge(...)
	local out = {}
	for _, t in ipairs({ ... }) do
		for k, v in pairs(t) do
			out[k] = v
		end
	end
	return out
end

-- FIX 3: inject() — names the "push event to front of queue" operation.
-- Replaces the raw table.insert(p.queue, 1, event) idiom so the intent
-- is obvious at the call site.
local function inject(p, event)
	table.insert(p.queue, 1, event)
end

-- ─────────────────────────────────────────────
-- Lint
-- ─────────────────────────────────────────────

local function lint(rules, initial)
	local referenced = {}

	for state, rule in pairs(rules) do
		-- FIX 4: single guard replaces the double-check anti-pattern.
		-- Old code did: if not transitions then warn; end; if transitions then loop end
		-- The inner branch could never be false — one guard is enough.
		if not rule.transitions or next(rule.transitions) == nil then
			print("WARNING: dead end state -> " .. state)
		else
			for _, target in pairs(rule.transitions) do
				if type(target) == "string" then
					if not rules[target] then
						print("WARNING: ghost state -> " .. target .. " (from " .. state .. ")")
					end
					referenced[target] = true
				end
			end
		end
	end

	for state, _ in pairs(rules) do
		if state ~= initial and not referenced[state] then
			print("WARNING: unreachable state -> " .. state)
		end
	end
end

-- ─────────────────────────────────────────────
-- Rules
-- ─────────────────────────────────────────────

-- Shared exits that every combat state needs — defined once, merged in.
local combat_exits = { hit = "staggered", die = "dead" }

local rpg_rules = {
	idle = {
		action = say("is idling. HP: {hp}"),
		transitions = merge({ walk = "moving", attack = "attacking" }, combat_exits),
	},

	moving = {
		action = say("is walking forward."),
		transitions = merge({ stop = "idle", attack = "attacking" }, combat_exits),
	},

	attacking = {
		action = say("swings their weapon!"),
		transitions = merge({ recover = "idle" }, combat_exits),
	},

	staggered = {
		action = function(p)
			local dmg = table.remove(p.damage_queue, 1) or 0
			p.hp = p.hp - dmg
			p.dmg = dmg -- expose to say() placeholder
			say("took {dmg} damage! HP is now {hp}")(p)

			if p.hp <= 0 then
				print("   > SYSTEM: Fatal damage detected! Injecting 'die' event...")
				inject(p, "die") -- FIX 3 in use
			end
		end,
		transitions = { recover = "idle", die = "dead" },
	},

	dead = {
		action = say("has collapsed to the ground."),
		transitions = { revive = "idle" },
	},
}

-- ─────────────────────────────────────────────
-- Payload
-- ─────────────────────────────────────────────

local my_payload = {
	name = "Hero",
	hp = 100,
	trace = {},
	queue = {
		"walk",
		"attack",
		"recover",
		"hit",
		"recover",
		"walk",
		"attack",
		"hit",
		"walk", -- They die on the second hit; this "walk" will be ignored.
	},
	damage_queue = { 15, 90 },
}

-- ─────────────────────────────────────────────
-- Entry point
-- ─────────────────────────────────────────────

if arg[1] == "--dot" then
	print(machine.to_dot(rpg_rules))
	os.exit()
end

print("=== STARTING TCO RPG BATTLE ===")
lint(rpg_rules, "idle")

local final_memory = machine.start(rpg_rules, "idle", my_payload)

print("\n--- FSM TRACE ---")
for _, t in ipairs(final_memory.trace) do
	print(t)
end

print("\n=== PROCESSING COMPLETE ===")
print("Final Queue Size remaining: " .. #final_memory.queue)
print("Final HP: " .. final_memory.hp)
