-- C1

-- C2
function select(t, f)
  local result = {}

  for _, v in ipairs(t) do
    if f(v) then
      table.insert(result, v)
    end
  end
  return result
end

-- C3

-- C4
function inject(t, acc, f)
  for _, v in ipairs(t) do
    acc = f(acc, t[v])
  end

  return acc
end

-- C5

-- C6
function range(start, stop, step)
  local current = start - step

  return function()
    current = current + step
    if current > stop then
      return nil
    end

    return current
  end
end

-- Test Helper function
function print_table(t)
  io.write("{")
  for i, v in ipairs(t) do
    io.write(v)
    if i < #t then
      io.write(", ")
    end
  end
  io.write("}\n")
end

-- Tests
-- C1 Test

-- C2 Test
local select_test = select({ 1, 2, 3, 4, 5 }, function(x) return x % 2 == 0 end)
print_table(select_test)

-- C3 Test

-- C4 Tests
local inject_test_1 = inject({ 1, 2, 3, 4 }, 0, function(a, x) return a + x end)
print(inject_test_1)

local inject_test_2 = inject({ 1, 2, 3, 4 }, 1, function(a, x) return a * x end)
print(inject_test_2)

-- C5 Test

-- C6 Test
for x in range(1, 10, 2) do print(x) end
