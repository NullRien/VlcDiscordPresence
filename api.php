<?php
// Define the password for authentication
define('UPLOAD_PASSWORD', 'secure_password');

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verify the password
    $password = $_POST['password'] ?? '';
    if ($password !== UPLOAD_PASSWORD) {
        http_response_code(403);
        echo json_encode(['status' => false, 'message' => 'Invalid password.']);
        exit;
    }

    // Check if a file is uploaded
    if (!isset($_FILES['image']) || $_FILES['image']['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['status' => false, 'message' => 'No file uploaded or an upload error occurred.']);
        exit;
    }

    // Get file details
    $uploadedFile = $_FILES['image'];
    $originalFilename = basename($uploadedFile['name']);
    $fileExtension = pathinfo($originalFilename, PATHINFO_EXTENSION);

    // Generate a unique filename
    $uniqueFilename = time() . "_" . uniqid() . "." . $fileExtension;
    $targetPath = getcwd() . DIRECTORY_SEPARATOR . $uniqueFilename;

    // Delete existing images
    foreach (glob(getcwd() . "/*.{jpg,png,gif}", GLOB_BRACE) as $existingFile) {
        if (is_file($existingFile)) {
            unlink($existingFile); // Delete the file
        }
    }

    // Validate file type (e.g., allow only images)
    $allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!in_array(mime_content_type($uploadedFile['tmp_name']), $allowedTypes)) {
        http_response_code(400);
        echo json_encode(['status' => false, 'message' => 'Invalid file type. Only images are allowed.']);
        exit;
    }

    // Move the uploaded file to the current directory
    if (move_uploaded_file($uploadedFile['tmp_name'], $targetPath)) {
        $fileUrl = "http://" . $_SERVER['HTTP_HOST'] . dirname($_SERVER['PHP_SELF']) . '/' . $uniqueFilename;
        echo json_encode(['status' => true, 'message' => 'File uploaded successfully.', 'url' => $fileUrl]);
    } else {
        http_response_code(500);
        echo json_encode(['status' => false, 'message' => 'Failed to save the file.']);
    }
} else {
    http_response_code(405);
    echo json_encode(['status' => false, 'message' => 'Invalid request method. Use POST.']);
}
?>
