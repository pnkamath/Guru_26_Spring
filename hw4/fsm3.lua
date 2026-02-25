local M = {}

local function run(rules, s, p)
	if rules[s] and rules[s].action then
		rules[s].action(p)
	end
	local e = table.remove(p.queue, 1)
	if not e then
		return p
	end
	return run(rules, (rules[s].transitions[e] or s), p)
end

function M.start(rules, s, p)
	return run(rules, s, p)
end

return M
