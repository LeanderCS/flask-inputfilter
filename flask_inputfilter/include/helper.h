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

class HttpMethodSet {
private:
    std::unordered_set<std::string> methods;

public:
    HttpMethodSet() = default;

    HttpMethodSet(const HttpMethodSet& other) : methods(other.methods) {}

    HttpMethodSet(HttpMethodSet&& other) noexcept : methods(std::move(other.methods)) {}

    HttpMethodSet& operator=(const HttpMethodSet& other) {
        if (this != &other) {
            methods = other.methods;
        }
        return *this;
    }

    HttpMethodSet& operator=(HttpMethodSet&& other) noexcept {
        if (this != &other) {
            methods = std::move(other.methods);
        }
        return *this;
    }

    explicit HttpMethodSet(const std::vector<std::string>& method_list) {
        methods.reserve(method_list.size());
        for (const auto& method : method_list) {
            methods.insert(method);
        }
    }

    bool contains(const std::string& method) const {
        return methods.find(method) != methods.end();
    }

    void add(const std::string& method) {
        methods.insert(method);
    }

    void clear() {
        methods.clear();
    }

    size_t size() const {
        return methods.size();
    }

    void from_vector(const std::vector<std::string>& method_list) {
        clear();
        methods.reserve(method_list.size());
        for (const auto& method : method_list) {
            methods.insert(method);
        }
    }
};

class StringConstants {
private:
    std::unordered_map<std::string, const char*> constants;
    static StringConstants& get_instance() {
        static StringConstants instance;
        return instance;
    }

    StringConstants() {
        constants["_condition"] = "_condition";
        constants["_error"] = "_error";
        constants["copy"] = "copy";
        constants["default"] = "default";
        constants["DELETE"] = "DELETE";
        constants["external_api"] = "external_api";
        constants["fallback"] = "fallback";
        constants["filters"] = "filters";
        constants["GET"] = "GET";
        constants["PATCH"] = "PATCH";
        constants["POST"] = "POST";
        constants["PUT"] = "PUT";
        constants["required"] = "required";
        constants["steps"] = "steps";
        constants["validators"] = "validators";
    }

public:
    static const char* get(const std::string& key) {
        auto& instance = get_instance();
        auto it = instance.constants.find(key);
        return (it != instance.constants.end()) ? it->second : nullptr;
    }

    static bool has(const std::string& key) {
        auto& instance = get_instance();
        return instance.constants.find(key) != instance.constants.end();
    }
};

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
