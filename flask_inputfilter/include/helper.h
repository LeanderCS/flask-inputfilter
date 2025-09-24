#ifndef HELPER_H
#define HELPER_H

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <memory>
#include <algorithm>

inline std::vector<std::string> make_default_methods() {
    return {
        "GET",
        "POST",
        "PATCH",
        "PUT",
        "DELETE"
    };
}

namespace string_ops {
    inline bool fast_startswith(const std::string& str, const std::string& prefix) {
        return str.size() >= prefix.size() &&
               str.compare(0, prefix.size(), prefix) == 0;
    }

    inline std::string fast_encode_utf8(const char* data, size_t len) {
        return std::string(data, len);
    }
}

template<typename T>
class ObjectPool {
private:
    std::vector<std::unique_ptr<T>> pool;
    size_t next_available = 0;
    static constexpr size_t DEFAULT_CAPACITY = 64;

public:
    ObjectPool() {
        pool.reserve(DEFAULT_CAPACITY);
    }

    T* acquire() {
        if (next_available < pool.size()) {
            return pool[next_available++].get();
        }
        pool.emplace_back(std::unique_ptr<T>(new T()));
        return pool[next_available++].get();
    }

    void release(T* obj) {
        if (next_available > 0) {
            --next_available;
        }
    }

    bool is_empty() const {
        return next_available == 0;
    }

    void release_all() {
        next_available = 0;
    }

    void reserve(size_t capacity) {
        pool.reserve(capacity);
    }

    size_t size() const {
        return pool.size();
    }

    size_t available() const {
        return pool.size() - next_available;
    }
};

class FieldLookup {
private:
    std::unordered_map<std::string, size_t> field_indices;
    std::vector<std::string> field_names;

public:
    void add_field(const std::string& name) {
        if (field_indices.find(name) == field_indices.end()) {
            field_indices[name] = field_names.size();
            field_names.push_back(name);
        }
    }

    bool has_field(const std::string& name) const {
        return field_indices.find(name) != field_indices.end();
    }

    size_t get_index(const std::string& name) const {
        auto it = field_indices.find(name);
        return (it != field_indices.end()) ? it->second : SIZE_MAX;
    }

    bool has_field_by_index(size_t index) const {
        return index < field_names.size();
    }

    const std::vector<std::string>& get_field_names() const {
        return field_names;
    }

    void clear() {
        field_indices.clear();
        field_names.clear();
    }

    void reserve(size_t capacity) {
        field_indices.reserve(capacity);
        field_names.reserve(capacity);
    }
};

class StringIntern {
private:
    static std::unordered_set<std::string>& get_strings() {
        static std::unordered_set<std::string> interned_strings;
        return interned_strings;
    }

public:
    static const std::string& intern(const std::string& str) {
        auto& strings = get_strings();
        auto result = strings.insert(str);
        return *result.first;
    }

    static void clear() {
        get_strings().clear();
    }

    static size_t count() {
        return get_strings().size();
    }
};

#endif
