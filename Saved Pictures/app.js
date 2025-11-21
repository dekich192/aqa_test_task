const express = require("express");
const app = express();

// Middleware
app.use(express.json());

// Инициализация данных
let users = [
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" }
];
let nextId = 3;

// Вспомогательные функции
const findUserById = (id) => users.find(user => user.id === id);
const findUserIndex = (id) => users.findIndex(user => user.id === id);

// Валидация
const validateUser = (user, isUpdate = false) => {
    const errors = [];
    
    if (!isUpdate || user.name !== undefined) {
        if (!user.name || user.name.trim() === '') {
            errors.push("Name is required");
        } else if (user.name.length > 50) {
            errors.push("Name must not exceed 50 characters");
        }
    }
    
    if (!isUpdate || user.email !== undefined) {
        if (!user.email || user.email.trim() === '') {
            errors.push("Email is required");
        } else if (!/\S+@\S+\.\S+/.test(user.email)) {
            errors.push("Email format is invalid");
        }
    }
    
    return errors;
};

// Middleware для логирования
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Маршруты

// GET /users - Получить всех пользователей
app.get("/users", (req, res) => {
    try {
        res.json({
            success: true,
            data: users,
            count: users.length
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// GET /users/:id - Получить пользователя по ID
app.get("/users/:id", (req, res) => {
    try {
        const id = parseInt(req.params.id);
        
        if (isNaN(id)) {
            return res.status(400).json({
                success: false,
                message: "Invalid ID format"
            });
        }
        
        const user = findUserById(id);
        
        if (!user) {
            return res.status(404).json({
                success: false,
                message: "User not found"
            });
        }
        
        res.json({
            success: true,
            data: user
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// POST /users - Создать нового пользователя
app.post("/users", (req, res) => {
    try {
        const { name, email } = req.body;
        
        // Валидация
        const validationErrors = validateUser({ name, email });
        if (validationErrors.length > 0) {
            return res.status(400).json({
                success: false,
                message: "Validation failed",
                errors: validationErrors
            });
        }
        
        // Проверка уникальности email
        const existingUser = users.find(user => user.email === email);
        if (existingUser) {
            return res.status(409).json({
                success: false,
                message: "User with this email already exists"
            });
        }
        
        // Создание пользователя
        const newUser = {
            id: nextId++,
            name: name.trim(),
            email: email.trim(),
            createdAt: new Date().toISOString()
        };
        
        users.push(newUser);
        
        res.status(201).json({
            success: true,
            message: "User created successfully",
            data: newUser
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// PUT /users/:id - Полное обновление пользователя
app.put("/users/:id", (req, res) => {
    try {
        const id = parseInt(req.params.id);
        
        if (isNaN(id)) {
            return res.status(400).json({
                success: false,
                message: "Invalid ID format"
            });
        }
        
        const userIndex = findUserIndex(id);
        
        if (userIndex === -1) {
            return res.status(404).json({
                success: false,
                message: "User not found"
            });
        }
        
        const { name, email } = req.body;
        
        // Валидация для полного обновления
        const validationErrors = validateUser({ name, email });
        if (validationErrors.length > 0) {
            return res.status(400).json({
                success: false,
                message: "Validation failed",
                errors: validationErrors
            });
        }
        
        // Проверка уникальности email (исключая текущего пользователя)
        const existingUser = users.find(user => user.email === email && user.id !== id);
        if (existingUser) {
            return res.status(409).json({
                success: false,
                message: "User with this email already exists"
            });
        }
        
        // Обновление пользователя
        users[userIndex] = {
            ...users[userIndex],
            name: name.trim(),
            email: email.trim(),
            updatedAt: new Date().toISOString()
        };
        
        res.json({
            success: true,
            message: "User updated successfully",
            data: users[userIndex]
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// PATCH /users/:id - Частичное обновление пользователя
app.patch("/users/:id", (req, res) => {
    try {
        const id = parseInt(req.params.id);
        
        if (isNaN(id)) {
            return res.status(400).json({
                success: false,
                message: "Invalid ID format"
            });
        }
        
        const userIndex = findUserIndex(id);
        
        if (userIndex === -1) {
            return res.status(404).json({
                success: false,
                message: "User not found"
            });
        }
        
        const { name, email } = req.body;
        
        // Валидация для частичного обновления
        const validationErrors = validateUser({ name, email }, true);
        if (validationErrors.length > 0) {
            return res.status(400).json({
                success: false,
                message: "Validation failed",
                errors: validationErrors
            });
        }
        
        // Проверка уникальности email для частичного обновления
        if (email) {
            const existingUser = users.find(user => user.email === email && user.id !== id);
            if (existingUser) {
                return res.status(409).json({
                    success: false,
                    message: "User with this email already exists"
                });
            }
        }
        
        // Частичное обновление
        const updatedUser = {
            ...users[userIndex],
            ...(name && { name: name.trim() }),
            ...(email && { email: email.trim() }),
            updatedAt: new Date().toISOString()
        };
        
        users[userIndex] = updatedUser;
        
        res.json({
            success: true,
            message: "User updated successfully",
            data: updatedUser
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// DELETE /users/:id - Удалить пользователя
app.delete("/users/:id", (req, res) => {
    try {
        const id = parseInt(req.params.id);
        
        if (isNaN(id)) {
            return res.status(400).json({
                success: false,
                message: "Invalid ID format"
            });
        }
        
        const userIndex = findUserIndex(id);
        
        if (userIndex === -1) {
            return res.status(404).json({
                success: false,
                message: "User not found"
            });
        }
        
        // Удаление пользователя
        const deletedUser = users.splice(userIndex, 1)[0];
        
        res.json({
            success: true,
            message: "User deleted successfully",
            data: deletedUser
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Internal server error",
            error: error.message
        });
    }
});

// Обработка несуществующих маршрутов
app.use("*", (req, res) => {
    res.status(404).json({
        success: false,
        message: "Route not found"
    });
});

// Глобальный обработчик ошибок
app.use((error, req, res, next) => {
    console.error("Unhandled error:", error);
    res.status(500).json({
        success: false,
        message: "Internal server error",
        error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});