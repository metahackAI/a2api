package demo;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

record Item(String id, String name, String internalNote) {}
record ItemView(String id, String name) {}
record NewItem(@NotBlank String name) {}
record PatchItem(String name) {}
record Filter(String q) {}

@RestController
@RequestMapping("/items")
public class ItemController {
    private final ConcurrentHashMap<String, Item> items = new ConcurrentHashMap<>();
    private final AtomicInteger sequence = new AtomicInteger(100);

    public ItemController() { items.put("I-1", new Item("I-1", "original", "server-only")); }

    private Item require(String id) {
        Item item = items.get(id);
        if (item == null) throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        return item;
    }

    @GetMapping("/{id}")
    public Item get(@PathVariable String id) { return require(id); }

    @RequestMapping(value = "/{id}", method = RequestMethod.HEAD)
    public void head(@PathVariable String id) { require(id); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Item create(@RequestBody @Valid NewItem body) {
        String id = "I-" + sequence.incrementAndGet();
        Item item = new Item(id, body.name(), "server-only");
        items.put(id, item);
        return item;
    }

    @PutMapping("/{id}")
    public Item replace(@PathVariable String id, @RequestBody @Valid NewItem body) {
        require(id);
        Item item = new Item(id, body.name(), "server-only");
        items.put(id, item);
        return item;
    }

    @PatchMapping("/{id}")
    public Item patch(@PathVariable String id, @RequestBody PatchItem body) {
        Item previous = require(id);
        Item item = new Item(id, body.name() == null ? previous.name() : body.name(), "server-only");
        items.put(id, item);
        return item;
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void remove(@PathVariable String id) { require(id); items.remove(id); }

    @PostMapping("/search")
    public List<ItemView> search(@RequestBody Filter body) {
        return items.values().stream().filter(item -> body.q() == null || item.name().contains(body.q()))
            .map(item -> new ItemView(item.id(), item.name())).toList();
    }
}
