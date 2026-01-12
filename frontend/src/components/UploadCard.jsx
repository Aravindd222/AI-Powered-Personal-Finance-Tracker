export default function UploadCard({ onUpload }) {
  return (
    <div className="bg-zinc-900 p-6 rounded-xl space-y-4">
      <input type="file" onChange={(e) => onUpload(e.target.files[0])} />

      <button className="bg-green-600 w-full py-2 rounded text-white" onClick={handleUpload}>
        Upload & Extract
      </button>
    </div>
  );
}
