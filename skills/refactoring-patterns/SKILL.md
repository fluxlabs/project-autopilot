---
name: refactoring-patterns
description: Safe refactoring techniques, code smell detection, and transformation patterns. Reference this skill when refactoring code.
---

# Refactoring Patterns Skill
# Project Autopilot - Safe refactoring techniques
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for safe, effective code refactoring.

---

## Refactoring Principles

### Safety First

1. **Test Before** - Ensure tests pass before refactoring
2. **Small Steps** - One change at a time
3. **Test After** - Verify behavior unchanged
4. **Version Control** - Commit frequently

### When to Refactor

| Trigger | Action |
|---------|--------|
| Adding feature | Refactor first if code resists change |
| Fixing bug | Refactor to make bug obvious |
| Code review | Refactor based on feedback |
| Comprehension | Refactor when you finally understand |

---

## Code Smells

### Bloaters

#### Long Method
**Symptom:** Method > 20 lines
**Solution:** Extract Method

```typescript
// Before: 50-line function
function processOrder(order: Order) {
  // validation (10 lines)
  // calculation (15 lines)
  // persistence (10 lines)
  // notification (15 lines)
}

// After: Extracted methods
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  await saveOrder(order, total);
  await notifyCustomer(order);
}
```

#### Large Class
**Symptom:** Class with many responsibilities
**Solution:** Extract Class

```typescript
// Before: God class
class UserManager {
  createUser() {}
  validateUser() {}
  sendEmail() {}
  generateReport() {}
  processPayment() {}
}

// After: Single responsibility
class UserService {
  createUser() {}
  validateUser() {}
}

class EmailService {
  sendEmail() {}
}

class PaymentService {
  processPayment() {}
}
```

#### Primitive Obsession
**Symptom:** Using primitives instead of small objects
**Solution:** Replace Primitive with Object

```typescript
// Before
function createUser(
  name: string,
  email: string,
  street: string,
  city: string,
  zip: string
) {}

// After
interface Address {
  street: string;
  city: string;
  zip: string;
}

function createUser(name: string, email: string, address: Address) {}
```

### Object-Orientation Abusers

#### Switch Statements
**Symptom:** Complex switch/if-else chains
**Solution:** Replace with Polymorphism

```typescript
// Before
function calculateShipping(type: string, weight: number) {
  switch (type) {
    case 'standard': return weight * 1.0;
    case 'express': return weight * 2.5;
    case 'overnight': return weight * 5.0;
    default: return weight * 1.0;
  }
}

// After
interface ShippingStrategy {
  calculate(weight: number): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(weight: number) { return weight * 1.0; }
}

class ExpressShipping implements ShippingStrategy {
  calculate(weight: number) { return weight * 2.5; }
}

const strategies: Record<string, ShippingStrategy> = {
  standard: new StandardShipping(),
  express: new ExpressShipping(),
};
```

### Change Preventers

#### Divergent Change
**Symptom:** One class changed for different reasons
**Solution:** Extract Class

#### Shotgun Surgery
**Symptom:** One change requires many small changes
**Solution:** Move Method, Move Field

```typescript
// Before: Changes to pricing require updates everywhere
class Order {
  calculatePrice() { /* includes tax logic */ }
}

class Invoice {
  generateTotal() { /* includes tax logic */ }
}

class Report {
  showPrices() { /* includes tax logic */ }
}

// After: Centralized
class TaxCalculator {
  static calculate(amount: number, region: string): number {
    // Single source of truth
  }
}
```

### Dispensables

#### Dead Code
**Symptom:** Unused code
**Solution:** Delete it

```typescript
// Before
function legacyFunction() {
  // Not called anywhere
}

const UNUSED_CONSTANT = 'never used';

// After: Simply remove
```

#### Speculative Generality
**Symptom:** "We might need this someday"
**Solution:** Remove unused abstraction

```typescript
// Before: Over-engineered for "future" needs
interface IUserRepository<T extends User> {
  find<K extends keyof T>(criteria: Partial<Pick<T, K>>): Promise<T[]>;
}

// After: What you actually need
interface UserRepository {
  findById(id: string): Promise<User>;
  findByEmail(email: string): Promise<User>;
}
```

### Couplers

#### Feature Envy
**Symptom:** Method uses another class's data more than its own
**Solution:** Move Method

```typescript
// Before: Method envies Order's data
class Invoice {
  calculateTotal(order: Order) {
    return order.items.reduce((sum, item) =>
      sum + item.price * item.quantity, 0
    );
  }
}

// After: Method belongs to Order
class Order {
  calculateTotal() {
    return this.items.reduce((sum, item) =>
      sum + item.price * item.quantity, 0
    );
  }
}
```

---

## Refactoring Catalog

### Extract Method

**When:** Code fragment that can be grouped together
**Mechanics:**
1. Create new method with descriptive name
2. Copy extracted code to new method
3. Scan for local variables
4. Pass as parameters if needed
5. Replace original code with method call

```typescript
// Before
function printOwing(invoice: Invoice) {
  printBanner();

  // Calculate outstanding
  let outstanding = 0;
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // Print details
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}

// After
function printOwing(invoice: Invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function calculateOutstanding(invoice: Invoice): number {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(invoice: Invoice, outstanding: number) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

### Inline Method

**When:** Method body is as clear as its name
**Mechanics:**
1. Check method isn't overridden
2. Find all calls
3. Replace each call with method body
4. Delete method

```typescript
// Before
function getRating(driver: Driver): number {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver: Driver): boolean {
  return driver.lateDeliveries > 5;
}

// After
function getRating(driver: Driver): number {
  return driver.lateDeliveries > 5 ? 2 : 1;
}
```

### Extract Variable

**When:** Complex expression hard to understand
**Mechanics:**
1. Create variable for expression/part
2. Replace expression with variable
3. Use descriptive name

```typescript
// Before
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);

// After
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

### Rename Variable/Method/Class

**When:** Name doesn't reveal purpose
**Mechanics:**
1. Check for existing uses
2. Update declaration
3. Update all references
4. Update documentation

```typescript
// Before
const d = new Date();
function calc(a, b) { return a * b; }

// After
const orderDate = new Date();
function calculateTotal(quantity, price) { return quantity * price; }
```

### Move Method

**When:** Method used more by another class
**Mechanics:**
1. Copy method to target class
2. Turn source into delegating method
3. Adjust for new context
4. Remove original

```typescript
// Before: Method on wrong class
class Account {
  overdraftCharge(): number {
    if (this.type.isPremium()) {
      return this.daysOverdrawn * 1.75;
    }
    return this.daysOverdrawn * 2.0;
  }
}

// After: Moved to AccountType
class AccountType {
  overdraftCharge(daysOverdrawn: number): number {
    if (this.isPremium()) {
      return daysOverdrawn * 1.75;
    }
    return daysOverdrawn * 2.0;
  }
}
```

### Replace Conditional with Polymorphism

**When:** Conditional varies behavior by type
**Mechanics:**
1. Create class hierarchy
2. Move conditional branches to subclasses
3. Replace conditionals with method calls

```typescript
// Before
function plumage(bird: Bird): string {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return 'average';
    case 'AfricanSwallow':
      return bird.numberOfCoconuts > 2 ? 'tired' : 'average';
    case 'NorwegianBlueParrot':
      return bird.voltage > 100 ? 'scorched' : 'beautiful';
    default:
      return 'unknown';
  }
}

// After
abstract class Bird {
  abstract get plumage(): string;
}

class EuropeanSwallow extends Bird {
  get plumage() { return 'average'; }
}

class AfricanSwallow extends Bird {
  get plumage() {
    return this.numberOfCoconuts > 2 ? 'tired' : 'average';
  }
}

class NorwegianBlueParrot extends Bird {
  get plumage() {
    return this.voltage > 100 ? 'scorched' : 'beautiful';
  }
}
```

---

## Modernization Transforms

### Callbacks to Async/Await

```typescript
// Before
function getData(callback) {
  fetch('/api/data')
    .then(response => response.json())
    .then(data => callback(null, data))
    .catch(error => callback(error));
}

// After
async function getData() {
  const response = await fetch('/api/data');
  return response.json();
}
```

### var to const/let

```typescript
// Before
var items = [];
for (var i = 0; i < 10; i++) {
  var item = createItem(i);
  items.push(item);
}

// After
const items = [];
for (let i = 0; i < 10; i++) {
  const item = createItem(i);
  items.push(item);
}
```

### String Concatenation to Templates

```typescript
// Before
const message = 'Hello, ' + user.name + '! You have ' + count + ' messages.';

// After
const message = `Hello, ${user.name}! You have ${count} messages.`;
```

### Function to Arrow Function

```typescript
// Before
const items = data.map(function(item) {
  return item.value;
});

// After
const items = data.map(item => item.value);
```

---

## Safety Checklist

### Before Refactoring

- [ ] Tests exist and pass
- [ ] Code is under version control
- [ ] Changes are committed
- [ ] Understand the code's purpose

### During Refactoring

- [ ] One refactoring at a time
- [ ] Run tests frequently
- [ ] Keep commits small
- [ ] Don't add features

### After Refactoring

- [ ] All tests still pass
- [ ] Behavior unchanged
- [ ] Code is cleaner
- [ ] Review the diff
