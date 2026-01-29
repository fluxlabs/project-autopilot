---
name: performance-analysis
description: Performance profiling patterns, optimization techniques, and benchmarking strategies. Reference this skill when analyzing performance.
---

# Performance Analysis Skill
# Project Autopilot - Profiling and optimization patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for performance analysis and optimization.

---

## Performance Metrics

### Core Web Vitals

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4s | >4s |
| FID (First Input Delay) | ≤100ms | ≤300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |
| INP (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |

### Backend Metrics

| Metric | Target |
|--------|--------|
| P50 Response Time | <100ms |
| P95 Response Time | <500ms |
| P99 Response Time | <1s |
| Error Rate | <0.1% |
| Throughput | Depends on scale |

### Database Metrics

| Metric | Target |
|--------|--------|
| Query Time | <50ms avg |
| Connection Pool Utilization | <80% |
| Index Hit Rate | >95% |
| Cache Hit Rate | >90% |

---

## Frontend Optimization

### Bundle Optimization

```typescript
// Code splitting with dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Route-based splitting
const routes = [
  {
    path: '/dashboard',
    component: lazy(() => import('./pages/Dashboard')),
  },
  {
    path: '/settings',
    component: lazy(() => import('./pages/Settings')),
  },
];

// Prefetching
<Link to="/dashboard" onMouseEnter={() => {
  import('./pages/Dashboard');
}}>
  Dashboard
</Link>
```

### Tree Shaking

```typescript
// ❌ Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Import specific function
import debounce from 'lodash/debounce';
debounce(fn, 300);

// ❌ Named imports from barrel file
import { Button, Input, Card } from '@/components';

// ✅ Direct imports
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

### Image Optimization

```tsx
// Next.js Image
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority          // Above the fold
  placeholder="blur"
  blurDataURL={blurUrl}
/>

// Lazy load below fold
<Image
  src="/feature.jpg"
  alt="Feature"
  loading="lazy"
/>

// Responsive images
<Image
  src="/product.jpg"
  alt="Product"
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### React Performance

```tsx
// Memoization
const ExpensiveComponent = memo(({ data }) => {
  return <div>{/* Expensive render */}</div>;
});

// useMemo for expensive calculations
const processedData = useMemo(() => {
  return expensiveCalculation(data);
}, [data]);

// useCallback for stable references
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Virtualization for long lists
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={400}
  itemCount={items.length}
  itemSize={35}
>
  {({ index, style }) => (
    <div style={style}>{items[index]}</div>
  )}
</FixedSizeList>
```

### Critical CSS

```html
<!-- Inline critical CSS -->
<head>
  <style>
    /* Critical above-the-fold styles */
    .hero { /* ... */ }
    .nav { /* ... */ }
  </style>

  <!-- Async load non-critical CSS -->
  <link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
</head>
```

---

## Backend Optimization

### Database Query Optimization

```typescript
// ❌ N+1 Query Problem
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } });
}
// Results in 1 + N queries

// ✅ Eager Loading
const users = await User.findAll({
  include: [{ model: Order }],
});
// Single query with JOIN

// ✅ Batch Loading
const users = await User.findAll();
const userIds = users.map(u => u.id);
const orders = await Order.findAll({
  where: { userId: { [Op.in]: userIds } }
});
// Group orders by userId manually
```

### Caching Strategies

```typescript
// Response caching
app.get('/api/products', async (req, res) => {
  const cacheKey = `products:${req.query.category}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return res.json(JSON.parse(cached));
  }

  // Fetch from database
  const products = await Product.findAll();

  // Cache for 5 minutes
  await redis.setex(cacheKey, 300, JSON.stringify(products));

  res.json(products);
});

// Cache invalidation
async function updateProduct(id, data) {
  await Product.update(data, { where: { id } });

  // Invalidate related caches
  await redis.del(`product:${id}`);
  await redis.del('products:*');
}
```

### Connection Pooling

```typescript
// PostgreSQL with pg
const pool = new Pool({
  max: 20,                    // Max connections
  min: 5,                     // Min connections
  idleTimeoutMillis: 30000,   // Close idle after 30s
  connectionTimeoutMillis: 2000,
  maxUses: 7500,              // Close after N uses
});

// Monitor pool health
setInterval(() => {
  console.log({
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount,
  });
}, 10000);
```

### Async Processing

```typescript
// ❌ Blocking in request
app.post('/api/orders', async (req, res) => {
  const order = await createOrder(req.body);
  await sendConfirmationEmail(order);    // Slow!
  await updateInventory(order);          // Slow!
  await notifyWarehouse(order);          // Slow!
  res.json(order);
});

// ✅ Queue for background processing
app.post('/api/orders', async (req, res) => {
  const order = await createOrder(req.body);

  // Queue background tasks
  await queue.add('send-confirmation', { orderId: order.id });
  await queue.add('update-inventory', { orderId: order.id });
  await queue.add('notify-warehouse', { orderId: order.id });

  res.json(order);
});
```

---

## Database Optimization

### Index Strategies

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index
CREATE INDEX idx_orders_pending ON orders(status)
WHERE status = 'pending';

-- Covering index
CREATE INDEX idx_products_search ON products(category_id, price)
INCLUDE (name, description);
```

### Query Optimization

```sql
-- ❌ Slow: Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2025;

-- ✅ Fast: Index-friendly
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';

-- ❌ Slow: SELECT *
SELECT * FROM users WHERE id = 123;

-- ✅ Fast: Select needed columns
SELECT id, name, email FROM users WHERE id = 123;

-- ❌ Slow: Subquery
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE status = 'active');

-- ✅ Fast: JOIN
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';
```

### Pagination

```typescript
// ❌ Offset pagination (slow for large offsets)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 10000;

// ✅ Cursor pagination (constant time)
SELECT * FROM products
WHERE id > $lastId
ORDER BY id
LIMIT 20;

// ✅ Keyset pagination with multiple columns
SELECT * FROM products
WHERE (created_at, id) > ($lastCreatedAt, $lastId)
ORDER BY created_at, id
LIMIT 20;
```

---

## Monitoring

### APM Integration

```typescript
// OpenTelemetry setup
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

### Custom Metrics

```typescript
// Histogram for response times
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

// Middleware to track
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });
  next();
});
```

---

## Performance Checklist

### Frontend

- [ ] Bundle size under budget
- [ ] Images optimized and lazy loaded
- [ ] Critical CSS inlined
- [ ] JavaScript code-split
- [ ] Fonts preloaded
- [ ] Third-party scripts async
- [ ] Service worker for caching

### Backend

- [ ] Database queries optimized
- [ ] Connection pooling configured
- [ ] Caching implemented
- [ ] Background jobs for slow tasks
- [ ] Compression enabled
- [ ] Keep-alive connections

### Database

- [ ] Indexes cover common queries
- [ ] No N+1 queries
- [ ] Pagination implemented
- [ ] Query plans analyzed
- [ ] Connection pool sized correctly
- [ ] Regular VACUUM/ANALYZE
