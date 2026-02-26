local M = {}

local function run(rules, s, p)
	local rule = rules[s]

	if rule and rule.action then
		rule.action(p)
	end

	local e = table.remove(p.queue, 1)
	if not e then
		return p
	end

	local trans

	if rule and rule.transitions then
		trans = rule.transitions[e] or rule.transitions["*"]
	end

	if type(trans) == "function" then
		trans = trans(p)
	end

	return run(rules, trans or s, p)
end

function M.start(rules, s, p)
	return run(rules, s, p)
end

function M.to_dot(rules)
	print("digraph fsm {")

	for state, rule in pairs(rules) do
		for event, target in pairs(rule.transitions or {}) do
			if type(target) == "string" then
				print(string.format('  %s -> %s [ label="%s" ]', state, target, event))
			else
				-- Guarded transitions (cannot statically resolve)
				print(string.format('  %s -> ??? [ label="%s (guard)" ]', state, event))
			end
		end
	end

	print("}")
end

return M
