const ProgressBar = ({ progress, isLoading }) => {
    const currentProgress = Math.max(progress, 1); // Ensure minimum visibility
    return (
        <div className={`progress-bar-container ${!isLoading && 'hide'}`}>
            <div className="progress-bar" style={{ width: `${currentProgress}%` }}></div>
        </div>
    );
};

export default ProgressBar;