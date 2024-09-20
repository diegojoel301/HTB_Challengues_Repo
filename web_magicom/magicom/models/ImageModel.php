<?php
class ImageModel {
    public function __construct($file) {
        $this->file = $file;
    }

    public function isValid() {

        $allowed_extensions = ["jpeg", "jpg", "png"];
        $file_extension = pathinfo($this->file["name"], PATHINFO_EXTENSION);
        // print_r($this->file); // Delete this
        if (!in_array($file_extension, $allowed_extensions)) {
            return false;
        }

        $allowed_mime_types = ["image/jpeg", "image/jpg", "image/png"];
        $mime_type = mime_content_type($this->file['tmp_name']);
        if (!in_array($mime_type, $allowed_mime_types)) {
            return false;
        }

        if (!getimagesize($this->file['tmp_name'])) {
            return false;
        }

        try {
            $imagick = new \Imagick($this->file['tmp_name']);
            $imagick->thumbnailImage(50, 50, true, true);
        } catch (Exception $e) {
            return false;
        }

        return true;
    }
}
?>
<?php
